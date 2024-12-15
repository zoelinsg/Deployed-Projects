from django import forms
from .models import Account, Category, Expense

# 帳戶表單
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']  # 表單欄位
        labels = {
            'name': '帳戶名稱',
            'balance': '帳戶餘額',
        }

# 記帳表單
class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # 使用 HTML5 日期輸入小部件

    class Meta:
        model = Expense
        fields = ['name', 'account', 'category', 'amount', 'is_income', 'date', 'notes']  # 表單欄位
        labels = {
            'name': '記帳項目名稱',
            'account': '帳戶',
            'category': '類別',
            'amount': '金額',
            'is_income': '收入',
            'date': '日期',
            'notes': '備註',
        }

# 轉帳表單
class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='轉出帳戶')
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='轉入帳戶')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='金額')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='日期')
    notes = forms.CharField(widget=forms.Textarea, required=False, label='備註')

# 篩選日期表單
class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='開始日期')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='結束日期')

# 篩選分類表單
class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='類別')