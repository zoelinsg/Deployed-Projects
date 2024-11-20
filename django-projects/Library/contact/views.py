from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from .forms import MessageForm
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 發送訊息視圖（讀者發送給館員）
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            # 假設所有館員的角色為 'librarian'
            librarians = User.objects.filter(profile__role='librarian')
            for librarian in librarians:
                Message.objects.create(sender=request.user, receiver=librarian, content=content)
            messages.success(request, "訊息已發送給所有館員。")
            return redirect('send_message')
    else:
        form = MessageForm()
    return render(request, 'library/send_message.html', {'form': form})

# 標記訊息為已讀或未讀視圖（館員）
@login_required
def toggle_read_status(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user.profile.role == 'librarian':
        if message.status == 'unread':
            message.status = 'read'
            messages.success(request, "訊息已標記為已讀。")
        else:
            message.status = 'unread'
            messages.success(request, "訊息已標記為未讀。")
        message.save()
    else:
        messages.error(request, "您沒有權限執行此操作。")
    return redirect('message_list')

# 封存訊息視圖（館員）
@login_required
def archive_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user.profile.role == 'librarian':
        message.archived = True
        message.status = 'read'  # 將訊息狀態改為已讀
        message.save()
        messages.success(request, "訊息已封存。")
    else:
        messages.error(request, "您沒有權限執行此操作。")
    return redirect('message_list')

# 解除封存訊息視圖（館員）
@login_required
def unarchive_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.user.profile.role == 'librarian':
        message.archived = False
        message.save()
        messages.success(request, "訊息已解除封存。")
    else:
        messages.error(request, "您沒有權限執行此操作。")
    return redirect('archived_message_list')

# 訊息列表視圖（館員）
@login_required
def message_list(request):
    if request.user.profile.role == 'librarian':
        messages = Message.objects.filter(receiver=request.user, archived=False).order_by('-timestamp')
        return render(request, 'library/message_list.html', {'messages': messages})
    else:
        messages.error(request, "您沒有權限查看此頁面。")
        return redirect('home')

# 封存訊息列表視圖（館員）
@login_required
def archived_message_list(request):
    if request.user.profile.role == 'librarian':
        messages = Message.objects.filter(receiver=request.user, archived=True).order_by('-timestamp')
        return render(request, 'library/archived_message_list.html', {'messages': messages})
    else:
        messages.error(request, "您沒有權限查看此頁面。")
        return redirect('home')