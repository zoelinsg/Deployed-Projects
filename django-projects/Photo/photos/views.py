from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from rest_framework import viewsets
from .forms import PhotoForm
from .models import Photo, Album, Category, Tag
from .serializers import PhotoSerializer, AlbumSerializer

# 上傳相片
@login_required
def upload_photos(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.author = request.user  # 設置相片作者為當前登入用戶
            photo.save()

            # 處理標籤
            tags_str = form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_str.split('#') if tag.strip()]
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                photo.tags.add(tag)

            return redirect('photo_list')  # 上傳成功後重定向到相片列表
    else:
        form = PhotoForm()
    return render(request, 'upload_photos.html', {'form': form})

# 相片列表
class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo_list.html'
    context_object_name = 'photos'

# 相片詳情
class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo_detail.html'
    context_object_name = 'photo'

# 編輯相片
class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    fields = ['title', 'description', 'image', 'album', 'category', 'location', 'tags']
    template_name = 'photo_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # 設置相片作者為當前登入用戶
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('photo_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.author  # 確認當前用戶是相片作者

# 刪除相片
class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('photo_list')  # 刪除成功後重定向到相片列表

    def test_func(self):
        photo = self.get_object()
        return self.request.user == photo.author  # 確認當前用戶是相片作者

# 相簿列表(首頁)
class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'home.html'  # 設置為首頁模板
    context_object_name = 'albums'

# 相簿詳情(單個相簿列出相簿中所有照片)
class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = Photo.objects.filter(album=self.get_object())  # 獲取相簿中的所有相片
        return context

# 新增相簿
class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['name', 'description']
    template_name = 'album_add.html'
    success_url = reverse_lazy('home')  # 新增成功後重定向到首頁

    def form_valid(self, form):
        form.instance.author = self.request.user  # 設置相簿作者為當前登入用戶
        return super().form_valid(form)

# 編輯相簿
class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    fields = ['name', 'description']
    template_name = 'album_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # 設置相簿作者為當前登入用戶
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.author  # 確認當前用戶是相簿作者

# 刪除相簿
class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'album_delete.html'
    success_url = reverse_lazy('home')  # 刪除成功後重定向到首頁

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.author  # 確認當前用戶是相簿作者
    
# 相片視圖集
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

# 相簿視圖集
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer