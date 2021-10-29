from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Question, Comment, Nice
from .serializers import QuestionSerializer, CommentSerializer, NiceSerializer
from .permissions import IsOwnerOnly
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """키워드 파라미터가 있을 경우 검색 가능"""
        queryset = Question.objects.all()
        keyword = self.request.query_params.get("keyword", None)
        if keyword is not None:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset

    def get_permissions(self):
        if self.action == "destroy":  # 삭제시 본인 또는 관리자(staff, superuser)여야 함.
            permission_classes = [IsOwnerOnly]
        elif self.action == "add_comment":  # 코멘트 작성시 인증 되어야 함.
            permission_classes = [IsAuthenticated]
        elif (
            self.action == "get_most_voted_question_in_the_month"
        ):  # 월별 가장 높은 좋아요 리스트 보려면 운영자여야 함
            permission_classes = [IsAdminUser]
        elif self.action == "get_comments":  # 코멘트는 누구나 볼 수 있다.
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        question = Question.objects.filter(pk=pk)
        if len(question) < 1:
            return Response(
                data={"error": "Question doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(question[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="most-voted")
    def get_most_voted_question_in_the_month(self, request, pk=None):
        """
        월별 가장 많은 좋아요를 받은 질문 목록을 출력한다.
        입력 받을 수 있는 query params
        from_year = 몇 년도부터 출력하는가
        from_month = 몇 월부터 출력하는가
        to_year = 몇 년도까지 출력하는가
        to_month = 몇 월까지 출력하는가
        """
        from_year = request.query_params.get("from_year", None)
        from_month = request.query_params.get("from_month", None)
        to_year = request.query_params.get("to_year", None)
        to_month = request.query_params.get("to_month", None)

        queryset = Question.objects.order_by(
            "-created_at__year", "-created_at__month", "-nice_count"
        ).distinct("created_at__year", "created_at__month")
        if from_year and from_month:
            queryset = queryset.filter(
                Q(created_at__year__gte=from_year)
                & Q(created_at__month__gte=from_month)
            )
        if to_year and to_month:
            queryset = queryset.filter(
                Q(created_at__year__lte=to_year) & Q(created_at__month__lte=to_month)
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True)
    def nices(self, request, pk=None):
        user = request.user
        serializer = NiceSerializer(user.nice.all(), many=True)
        return Response(serializer.data)

    @nices.mapping.put
    def toggle_nice(self, request, pk=None):
        user = request.user
        question = self.get_object()
        message = ""
        nice, _ = Nice.objects.get_or_create(user=user)

        if question not in nice.questions.all():
            # 질문이 유저의 좋아요 목록에 없을 경우
            question.add_nice_count()
            nice.questions.add(question)
            message = "좋아요에 추가되었습니다"
        else:
            question.remove_nice_count()
            nice.questions.remove(question)
            message = "좋아요를 해제하였습니다."
        nice.save()
        question.save()
        return Response(data={"message": message}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path="comments")
    def get_comments(self, request, pk=None):
        """질문에 대한 댓글 목록을 가져온다."""
        question = self.get_object()
        comments = Comment.objects.filter(question=question)
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True, url_path="add-comment")
    def add_comment(self, request, pk=None):
        """질문에 대한 댓글을 추가한다."""
        user_obj = get_user_model().objects.get(id=request.user.id)
        question = self.get_object()
        comment = Comment.objects.create(
            author=user_obj, question=question, text=request.data.get("text")
        )
        serializer = CommentSerializer(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
