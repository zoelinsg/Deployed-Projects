from django.core.management.base import BaseCommand
from faker import Faker
import random
from activity.models import Activity
from django.contrib.auth.models import User
from datetime import timedelta

class Command(BaseCommand):
    help = '生成指定數量的假活動資料'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='指定需要生成的活動數量'
        )

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker('zh_TW')
        LOCATION_CHOICES = ['3F多媒體室', '4F多功能室', '5樓大演講廳']
        users = list(User.objects.all())

        activity_to_create = []
        for _ in range(count):
            start_datetime = fake.date_time_this_year(before_now=False, after_now=True)
            end_datetime = start_datetime + timedelta(hours=random.randint(1, 5))

            activity = Activity(
                title=fake.sentence(nb_words=random.randint(2, 5)),
                start_date=start_datetime.date(),
                start_time=start_datetime.time(),
                end_date=end_datetime.date(),
                end_time=end_datetime.time(),
                created_by=random.choice(users),
                description=fake.paragraph(nb_sentences=random.randint(3, 6)),
                location=random.choice(LOCATION_CHOICES),
                speaker=fake.name() if random.choice([True, False]) else None
            )
            activity_to_create.append(activity)

        # 使用 bulk_create 一次性創建所有活動
        Activity.objects.bulk_create(activity_to_create)
        self.stdout.write(self.style.SUCCESS(f'成功生成 {count} 筆假活動資料'))