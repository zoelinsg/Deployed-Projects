from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 借自修室視圖（僅讀者）
@login_required
def borrow_room(request, pk):
    if request.user.profile.role != 'reader':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('room_list')
    
    # 檢查讀者是否已經借閱了一個房間
    if Room.objects.filter(borrowed_by=request.user, status='in_use').exists():
        messages.error(request, "您已經借閱了一個自修室，無法再借閱其他自修室。")
        return redirect('room_list')
    
    room = get_object_or_404(Room, pk=pk)
    if room.status == 'available':
        room.status = 'in_use'  # 將自修室狀態設置為使用中
        room.borrowed_by = request.user
        room.cancelled = False  # 重置取消預約狀態
        room.save()
        messages.success(request, "自修室借閱成功。")
    else:
        messages.error(request, "該自修室目前不可借閱。")
    return redirect('room_detail', pk=pk)

# 結束使用自修室視圖（僅讀者）
@login_required
def return_room(request, pk):
    if request.user.profile.role != 'reader':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('room_list')
    
    room = get_object_or_404(Room, pk=pk)
    if room.status == 'in_use' and room.borrowed_by == request.user:
        room.status = 'available'  # 將自修室狀態設置為可借閱
        room.borrowed_by = None
        room.cancelled = True  # 設置取消預約狀態
        room.save()
        messages.success(request, "自修室使用結束。")
    else:
        messages.error(request, "您無法結束使用此自修室。")
    return redirect('room_detail', pk=pk)

# 自修室列表視圖
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'library/room_list.html', {'rooms': rooms})

# 自修室詳情視圖
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'library/room_detail.html', {'room': room})