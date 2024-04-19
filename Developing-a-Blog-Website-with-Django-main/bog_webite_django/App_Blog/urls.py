from django.urls import path
from App_Blog import views
from django.conf import settings
from django.conf.urls.static import static




app_name = 'App_Blog'

urlpatterns = [
    path('', views.BlogList.as_view(), name='blog_list'),
    path('write/', views.CreateBlog.as_view(), name='create_blog'),
    path('details/<slug:slug>', views.blog_details, name='blog_details'),
    path('liked/<pk>/', views.liked, name='liked_post'),
    path('unliked/<pk>/', views.unliked, name='unliked_post'),
    path('my-blogs/', views.MyBlogs.as_view(), name='my_blogs'),
    path('edit/<pk>/', views.UpdateBlog.as_view(), name='edit_blog'),
    path('delete/<pk>/', views.DeleteBlog.as_view(), name='delete_blog'),
 

    path('search/', views.BlogSearchView.as_view(), name='search_blog'),
    path('blog-most-liked/',views.MostLikedBlogView.as_view(),name='most_liked_blog'),
    path('blog-most-cmt/',views.MostCommentedBlogView.as_view(),name='most_commented_blog'),
    
    path('upload/',views.UploadVideo.as_view(), name='upload_video'),
    path('uploadlist/',views.UploadList.as_view(),name='upload_list'),
    # path('delete_video/<int:pk>/',views.DeleteVideo.as_view(), name='delete_video'),
   
]
