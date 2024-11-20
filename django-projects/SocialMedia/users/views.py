from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount
from itertools import chain
import random

# 首頁視圖，顯示動態和使用者建議
@login_required(login_url='signin')
def index(request):
    # 取得當前登入的使用者
    user_object = User.objects.get(username=request.user.username)
    
    # 確保使用者的 Profile 已存在，如果沒有則創建
    user_profile, created = Profile.objects.get_or_create(user=user_object, defaults={'id_user': user_object.id})

    user_following_list = []
    feed = []

    # 查找當前使用者關注的所有使用者
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    # 將關注的使用者加入列表
    for users in user_following:
        user_following_list.append(users.user)

    # 獲取關注的使用者的文章，並加入動態列表
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    # 合併動態中的文章
    feed_list = list(chain(*feed))

    # 添加顯示當前使用者自己的文章 # 新增
    user_posts = Post.objects.filter(user=request.user.username)  # 新增
    feed_list.extend(user_posts)  # 新增

    # 開始生成使用者建議
    all_users = User.objects.all()
    user_following_all = []

    # 查找使用者關注的所有人，並將其加入列表
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    # 新的使用者建議列表：排除當前使用者已關注的人
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    # 排除當前登入的使用者
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    # 隨機打亂建議列表
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    # 取得使用者建議的 ID
    for users in final_suggestions_list:
        username_profile.append(users.id)

    # 根據 ID 取得對應的 Profile
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    # 合併使用者建議的資料
    suggestions_username_profile_list = list(chain(*username_profile_list))

    # 渲染 index.html，並傳遞使用者的資料、文章動態和建議列表
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

# 上傳文章的視圖
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        # 取得當前登入的使用者名稱和上傳的圖片及說明
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        # 創建並儲存新文章
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

# 搜尋功能的視圖
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        # 根據輸入的使用者名稱進行模糊搜尋
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        # 取得搜尋到的使用者 ID
        for users in username_object:
            username_profile.append(users.id)

        # 根據 ID 取得 Profile
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        # 合併搜尋結果
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

# 點讚功能的視圖
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    # 根據文章 ID 找到文章
    post = Post.objects.get(id=post_id)

    # 檢查該使用者是否已經點過讚
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        # 如果沒有點讚，則新增一條讚記錄並增加讚數
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        # 如果已點讚，則刪除點讚記錄並減少讚數
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')

# 使用者個人資料頁面視圖
@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    # 根據當前使用者是否已關注該使用者，顯示不同的按鈕
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    # 計算追蹤者和關注數量
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    # 傳遞資料給前端
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

# 關注和取消關注功能視圖
@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        # 檢查使用者是否已關注，若已關注則取消，否則新增關注
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return redirect('/')

# 使用者設定頁面的視圖
@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # 如果沒有上傳新頭像，使用原來的圖片
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        # 如果上傳了新頭像，更新使用者資料
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

# 註冊功能的視圖
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # 檢查兩次輸入的密碼是否一致
        if password == password2:
            # 檢查使用者名稱或電子郵件是否已被使用
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                # 創建新使用者並保存
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # 登入新使用者並跳轉至設定頁面
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # 為新使用者創建個人資料
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

# 登入功能的視圖
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 驗證使用者憑證並登入
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

# 登出功能的視圖
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
