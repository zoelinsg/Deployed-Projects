from django.db import models
from django.conf import settings

# 建立模型

class Account(models.Model):
    """帳戶模型"""
    name = models.CharField(max_length=100, verbose_name='帳戶名稱')  # 帳戶名稱
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts', verbose_name='用戶')  # 用戶
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='帳戶餘額')  # 帳戶餘額
    created = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')  # 建立時間
    updated = models.DateTimeField(auto_now=True, verbose_name='更新時間')  # 更新時間

    class Meta:
        verbose_name = '帳戶'
        verbose_name_plural = '帳戶'
        ordering = ('-updated',)  # 依更新時間排序

    def __str__(self):
        return self.name

class Category(models.Model):
    """類別模型"""
    name = models.CharField(max_length=100, verbose_name='類別名稱')  # 類別名稱

    class Meta:
        verbose_name = '類別'
        verbose_name_plural = '類別'
        ordering = ('-name',)  # 依名稱排序

    def __str__(self):
        return self.name

class Expense(models.Model):
    """記帳模型"""
    name = models.CharField(max_length=100, verbose_name='記帳項目名稱')  # 記帳項目名稱
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expenses', verbose_name='帳戶')  # 帳戶
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses', verbose_name='類別')  # 類別
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses', verbose_name='用戶')  # 用戶
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金額')  # 金額
    is_income = models.BooleanField(default=False, verbose_name='收入')  # 收入
    date = models.DateField(verbose_name='日期')  # 日期
    notes = models.TextField(blank=True, verbose_name='備註')  # 備註
    created = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')  # 建立時間
    updated = models.DateTimeField(auto_now=True, verbose_name='更新時間')  # 更新時間

    class Meta:
        verbose_name = '記帳'
        verbose_name_plural = '記帳'
        ordering = ('-date',)  # 依日期排序

    def __str__(self):
        return f'{self.account.name} - {self.category.name} - {self.amount} - {self.date}'

    @staticmethod
    def total_balance(user):
        """計算用戶所有帳戶的總餘額"""
        accounts = Account.objects.filter(user=user)
        total = sum(account.balance for account in accounts)
        return total