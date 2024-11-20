# 檔案: generate_books.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from books.models import Book

class Command(BaseCommand):
    help = '生成假書籍數據'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='要生成的書籍數量')

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker()
        CATEGORY_CHOICES = ['fiction', 'non-fiction', 'biography', 'reference', 'other']

        books_to_create = []
        for _ in range(count):
            book = Book(
                title=fake.sentence(nb_words=random.randint(2, 6)),
                author=fake.name(),
                category=random.choice(CATEGORY_CHOICES),
                description=fake.paragraph(nb_sentences=random.randint(3, 6)),
                publication_date=fake.date_between(start_date='-10y', end_date='today'),
                isbn=fake.isbn13(separator="-"),
                cover='covers/default_cover.jpg'  # 設置預設圖片
            )
            books_to_create.append(book)

        # 使用 bulk_create 一次性創建所有書籍
        Book.objects.bulk_create(books_to_create)
        self.stdout.write(self.style.SUCCESS(f'成功生成 {count} 筆假書籍資料'))