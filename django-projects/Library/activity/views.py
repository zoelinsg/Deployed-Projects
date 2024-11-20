from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Activity
from .forms import ActivityForm
from .serializers import ActivitySerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 創建活動視圖（僅館員）
@login_required
def create_activity(request):
    if request.user.profile.role != 'librarian':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('activity_list')
    
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            try:
                activity.save()
                messages.success(request, "活動已成功創建。")
                return redirect('activity_list')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ActivityForm()
    return render(request, 'library/create_activity.html', {'form': form})

# 更新活動視圖（僅館員）
@login_required
def update_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.user.profile.role != 'librarian':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('activity_list')
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "活動已成功更新。")
                return redirect('activity_detail', pk=pk)
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'library/update_activity.html', {'form': form, 'activity': activity})

# 刪除活動視圖（僅館員）
@login_required
def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.user.profile.role != 'librarian':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('activity_list')
    
    if request.method == 'POST':
        activity.delete()
        messages.success(request, "活動已成功刪除。")
        return redirect('activity_list')
    return render(request, 'library/delete_activity.html', {'activity': activity})

# 活動列表視圖
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, 'library/activity_list.html', {'activities': activities})

# 活動詳情視圖
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, 'library/activity_detail.html', {'activity': activity})

# 參與活動視圖（讀者）
@login_required
def participate_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.user.profile.role == 'reader':
        activity.participants.add(request.user)
        messages.success(request, "您已成功參與此活動。")
    else:
        messages.error(request, "您沒有權限執行此操作。")
    return redirect('activity_detail', pk=pk)

# 取消參加活動視圖（讀者）
@login_required
def cancel_participation(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.user.profile.role == 'reader':
        activity.participants.remove(request.user)
        messages.success(request, "您已取消參加此活動。")
    else:
        messages.error(request, "您沒有權限執行此操作。")
    return redirect('activity_detail', pk=pk)

# 活動 API 視圖
@api_view(['GET'])
def activity_api(request):
    activities = Activity.objects.all()
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)