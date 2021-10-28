from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q, Max, F
from django.shortcuts import get_object_or_404
from .models import Question, Comment, Nice
from .serializers import QuestionSerializer, CommentSerializer, NiceSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        keyword = self.request.query_params.get("keyword", None)
        if keyword is not None:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset

    def retrieve(self, request, pk=None):
        question = Question.objects.filter(pk=pk)
        if len(question) < 1:
            return Response(
                data={"error": "Question doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(question[0])
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="most-nice-per-month")
    def get_most_voted_question_in_the_month(self, request, pk=None):
        """월별 가장 많은 좋아요를 받은 질문 목록을 출력한다."""
        from_year = request.query_params.get("from_year", 2010)
        from_month = request.query_params.get("from_month", 1)
        this_time = datetime.now()
        current_year = this_time.year
        current_month = this_time.month
        # questions = Question.objects.filter(
        #     Q(created_at__year__lte=current_year)
        #     & Q(created_at__month__lte=current_month)
        # ).aggregate(nice_count_max=Max("nice_count"))

        # Question.objects.values("created_at__year", "created_at__month")
        # .annotate(
        #     nice_count=Max("nice_count"),
        #     year=F("created_at__year"),
        #     month=F("created_at__month"),
        # )
        # .values("nice_count", "year", "month", "title")
        # .values(
        #     "id", "created_at__year", "created_at__month", "nice_count"
        # )
        # queryset = Question.objects.all()
        # max_nices = queryset.values("id").annotate(most_voted=Max("nice_count"))
        # print(max_nices)
        # queryset = queryset.filter(id__in=max_nices)
        queryset = Question.objects.annotate(Max("nice_count"))
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True, url_path="user-nice")
    def user_nice(self, request, pk=None):
        user = request.user
        question = self.get_object()
        message = ""
        if question not in user.nice.questions:
            # 질문이 유저의 좋아요 목록에 없을 경우
            question.add_nice_count()
            user.nice.questions.add(question)
            message = "좋아요에 추가되었습니다"
        else:
            question.remove_nice_count()
            user.nice.questions.remove(question)
            message = "좋아요를 해제하였습니다."
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
