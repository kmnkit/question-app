import random
import datetime
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from questions.models import Question
from random import randrange

start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2021, 12, 31)

time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days


User = get_user_model()
sentences = [
    "The fox in the tophat whispered into the ear of the rabbit.",
    "My dentist tells me that chewing bricks is very bad for your teeth.",
    "Best friends are like old tomatoes and shoelaces.",
    "They say that dogs are man's best friend, but this cat was setting out to sabotage that theory.",
    "The miniature pet elephant became the envy of the neighborhood.",
    "He was surprised that his immense laziness was inspirational to others.",
    "You should never take advice from someone who thinks red paint dries quicker than blue paint.",
    "They finished building the road they knew no one would ever use.",
    "Don't step on the broken glass.",
    "They throw cabbage that turns your brain into emotional baggage.",
    "Before he moved to the inner city, he had always believed that security complexes were psychological.",
    "Hang on, my kittens are scratching at the bathtub and they'll upset by the lack of biscuits.",
    "It's much more difficult to play tennis with a bowling ball than it is to bowl with a tennis ball.",
    "It was at that moment that he learned there are certain parts of the body that you should never Nair.",
    "Tuesdays are free if you bring a gnome costume.",
    "The swirled lollipop had issues with the pop rock candy.",
    "She was amazed by the large chunks of ice washing up on the beach.",
    "Someone I know recently combined Maple Syrup & buttered Popcorn thinking it would taste like caramel popcorn. It didn’t and they don’t recommend anyone else do it either.",
    "The furnace repairman indicated the heating system was acting as an air conditioner.",
    "That was how he came to win $1 million.",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        author = User.objects.get(name="admin12")
        questions_list = []
        for _ in range(40):
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_number_of_days)
            sent_1 = random.choice(sentences)
            if len(sent_1) > 50:
                sent_1 = sent_1[:50]
            sent_2 = random.choice(sentences)
            questions_list.append(
                Question(
                    author=author,
                    title=sent_1,
                    text=sent_2,
                    nice_count=random.randint(1, 100),
                )
            )
        Question.objects.bulk_create(questions_list)
        self.stdout.write(self.style.SUCCESS("%d개의 질문 생성 완료" % 50))
