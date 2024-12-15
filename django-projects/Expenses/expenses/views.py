from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Expense, Category
from .forms import AccountForm, ExpenseForm, TransferForm, DateFilterForm, CategoryFilterForm

# 登入後只管理自己的帳目

@login_required
def home(request):
    """首頁，顯示用戶的所有帳戶和總餘額"""
    accounts = Account.objects.filter(user=request.user)
    total_balance = sum(account.balance for account in accounts)
    return render(request, 'expenses/home.html', {'accounts': accounts, 'total_balance': total_balance})

@login_required
def account_create(request):
    """新增帳戶"""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('home')
    else:
        form = AccountForm()
    return render(request, 'expenses/account_form.html', {'form': form})

@login_required
def account_edit(request, pk):
    """編輯帳戶"""
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AccountForm(instance=account)
    return render(request, 'expenses/account_form.html', {'form': form})

@login_required
def account_delete(request, pk):
    """刪除帳戶"""
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
        return redirect('home')
    return render(request, 'expenses/account_confirm_delete.html', {'account': account})

@login_required
def expense_list(request):
    """顯示用戶的所有記帳項目"""
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def account_expense_list(request, pk):
    """顯示單個帳戶的所有記帳項目"""
    account = get_object_or_404(Account, pk=pk, user=request.user)
    expenses = Expense.objects.filter(account=account)
    return render(request, 'expenses/account_expense_list.html', {'account': account, 'expenses': expenses})

@login_required
def expense_create(request):
    """新增記帳項目"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            # 更新帳戶餘額
            account = expense.account
            if expense.is_income:
                account.balance += expense.amount
            else:
                account.balance -= expense.amount
            account.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_edit(request, pk):
    """編輯記帳項目"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            old_amount = expense.amount
            old_is_income = expense.is_income
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            # 更新帳戶餘額
            account = expense.account
            if old_is_income:
                account.balance -= old_amount
            else:
                account.balance += old_amount
            if expense.is_income:
                account.balance += expense.amount
            else:
                account.balance -= expense.amount
            account.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_delete(request, pk):
    """刪除記帳項目"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        # 更新帳戶餘額
        account = expense.account
        if expense.is_income:
            account.balance -= expense.amount
        else:
            account.balance += expense.amount
        account.save()
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})

@login_required
def transfer(request):
    """轉帳功能"""
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']
            notes = form.cleaned_data['notes']

            # 更新轉出帳戶餘額
            from_account.balance -= amount
            from_account.save()

            # 更新轉入帳戶餘額
            to_account.balance += amount
            to_account.save()

            # 獲取或創建一個預設的轉帳類別
            transfer_category, created = Category.objects.get_or_create(name='轉帳')

            # 新增轉出記錄
            Expense.objects.create(
                name=f'轉帳至 {to_account.name}',
                account=from_account,
                category=transfer_category,
                user=request.user,
                amount=amount,
                is_income=False,
                date=date,
                notes=notes
            )

            # 新增轉入記錄
            Expense.objects.create(
                name=f'從 {from_account.name} 轉帳',
                account=to_account,
                category=transfer_category,
                user=request.user,
                amount=amount,
                is_income=True,
                date=date,
                notes=notes
            )

            return redirect('home')
    else:
        form = TransferForm()
    return render(request, 'expenses/transfer_form.html', {'form': form})

@login_required
def filter_by_date(request):
    """篩選日期顯示記帳項目"""
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            expenses = Expense.objects.filter(user=request.user, date__range=[start_date, end_date])
            return render(request, 'expenses/date_filter_form.html', {'form': form, 'expenses': expenses})
    else:
        form = DateFilterForm()
        expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/date_filter_form.html', {'form': form, 'expenses': expenses})

@login_required
def filter_by_category(request):
    """篩選分類顯示記帳項目"""
    if request.method == 'POST':
        form = CategoryFilterForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            expenses = Expense.objects.filter(user=request.user, category=category)
            return render(request, 'expenses/category_filter_form.html', {'form': form, 'expenses': expenses})
    else:
        form = CategoryFilterForm()
        expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/category_filter_form.html', {'form': form, 'expenses': expenses})