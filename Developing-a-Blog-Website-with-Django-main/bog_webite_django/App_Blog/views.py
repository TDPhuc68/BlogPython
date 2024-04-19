from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView,DeleteView
from App_Blog.models import Blog, Comment, Likes,Video
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from App_Blog.forms import CommentForm
import uuid
from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from.models import Post
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Video



# Create your views here.
# Create your views here.

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/my_blogs.html'

# 1 view được sử dụng để hiển thị một mẫu cho người dùng tạo blog mới trong ứng dụng Django.
class CreateBlog(LoginRequiredMixin, CreateView):
    #Thuộc tính này chỉ định model mà view này sẽ sử dụng để tạo đối tượng. 
    model = Blog       

    #Điều này chỉ định tên của tệp mẫu mà view này sẽ sử dụng để hiển thị giao diện người dùng. 
    template_name = 'App_Blog/create_blog.html'

    #Đây là một tuple của các trường từ model Blog mà người dùng có thể nhập dữ liệu trong mẫu. 
    fields = ('blog_title', 'blog_content', 'blog_image',) 

    def form_valid(self, form):
        # Lưu đối tượng Blog từ dữ liệu mẫu, nhưng không commit vào cơ sở dữ liệu
        blog_obj = form.save(commit=False) 
        # Gán tác giả của bài đăng là người dùng hiện tại

        blog_obj.author = self.request.user
        #Lấy tiêu đề của blog từ mẫu
        title = blog_obj.blog_title
        #Tạo slug cho blog, thay thế khoảng trắng bằng "-" và thêm một UUID duy nhất
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        #Lưu đối tượng Blog vào cơ sở dữ liệu
        blog_obj.save()
        #Chuyển hướng người dùng về trang chính sau khi tạo blog thành công
        return HttpResponseRedirect(reverse('index'))
    
#
#   
#hiển thị một danh sách các bài đăng bằng cách sử dụng một mẫu được chỉ định
class BlogList(ListView):
    
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 2

#
#
#
@login_required
def blog_details(request, slug):
    # # Lấy đối tượng Blog từ cơ sở dữ liệu dựa trên slug
    blog = Blog.objects.get(slug=slug)
    #Tạo một biểu mẫu mới cho phản hồi
    comment_form = CommentForm()
    # # Kiểm tra xem người dùng đã thích bài đăng này chưa
    already_liked = Likes.objects.filter(blog=blog, user= request.user)
    if already_liked:
        liked = True
    else:
        liked = False
    # Xử lý khi người dùng gửi một phản hồi mới
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
    # Chuyển hướng người dùng trở lại trang chi tiết bài đăng sau khi gửi phản hồi
            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':slug}))
    #Trả về trang chi tiết bài đăng với các thông tin cần thiết
    return render(request, 'App_Blog/blog_details.html', context={'blog':blog, 'comment_form':comment_form, 'liked':liked,})
#
#
# xử lý hành động của người dùng khi họ thích một bài đăng cụ thể.
@login_required
def liked(request, pk):
        # Lấy đối tượng Blog từ cơ sở dữ liệu dựa trên khóa chính (primary key)
    blog = Blog.objects.get(pk=pk)
         # Lấy thông tin người dùng hiện tại
    user = request.user
         # Kiểm tra xem người dùng đã thích bài đăng này chưa
    already_liked = Likes.objects.filter(blog=blog, user=user)
         # Nếu người dùng chưa thích bài đăng này
    if not already_liked:
         # Tạo một bản ghi mới trong bảng Likes đại diện cho sự thích của người dùng đối với bài đăng này
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
         # Chuyển hướng người dùng trở lại trang chi tiết bài đăng sau khi họ thích bài đăng
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug}))
#
#
# thêm và xóa việc thích một bài đăng
@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug':blog.slug}))
# một view dựa trên lớp trong Django
class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'App_Blog/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('App_Blog:blog_details', kwargs={'slug':self.object.slug})
    
class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('App_Blog:blog_list')
    template_name = 'App_Blog/delete_blog.html'

# class BlogSearchView(LoginRequiredMixin, ListView):
#     context_object_name = 'blogs'
#     model = Blog
#     template_name = 'App_Blog/search.html'

#     def get_queryset(self) :
#        query = self.request.GET.get('q')
#        queryset = Blog.objects.filter(blog_title__icontains=query).order_by('-blog_title')
class BlogSearchView(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            # Lọc bài đăng theo tiêu đề chứa từ khóa tìm kiếm
            queryset = Blog.objects.filter(blog_title__icontains=query).order_by('-blog_title')
        else:
            # Nếu không có từ khóa tìm kiếm, trả về tất cả các bài đăng
            queryset = Blog.objects.all()

        # Sắp xếp kết quả theo thời gian xuất bản giảm dần
        return queryset.order_by('-publish_date')
    
class MostLikedBlogView(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/most_liked_blog.html'

    def get_queryset(self):
        # Truy vấn để lấy bài blog có số lượt thích nhiều nhất
        most_liked_blog = Blog.objects.annotate(num_likes=Count('liked_blog')).order_by('-num_likes').first()
        return [most_liked_blog]
    
class MostCommentedBlogView(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/most_commented_blog.html'

    def get_queryset(self):
        # Truy vấn để lấy bài blog có số lượng comment nhiều nhất
        most_commented_blog = Blog.objects.annotate(num_comments=Count('blog_comment')).order_by('-num_comments').first()
        return [most_commented_blog]
class UploadVideo(LoginRequiredMixin, CreateView):
    model = Video
    template_name = 'App_Blog/upload_video.html'
    fields = ('caption', 'video',)

    def form_valid(self, form):
        video = form.save(commit=False)
        caption=video.caption
        video.save()
        return HttpResponseRedirect(reverse('index'))

class UploadList(ListView):
    context_object_name = 'videos'
    model = Video
    template_name = 'App_Blog/upload_list.html'  

# class DeleteVideo(LoginRequiredMixin,View) :
#     context_object_name = 'videos'
#     model = Video
#     template_name = 'App_Blog/upload_list.html'  

#     def delete_video(request, video_id):
#     # Lấy video dựa trên video_id
#         video = Video.objects.get(id=video_id)
#     # Xóa video
#         video.delete()
#     # Chuyển hướng người   dùng đến trang chính sau khi xóa
#         return redirect('home')



