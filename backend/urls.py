# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from django.conf import settings
# from django.conf.urls.static import static
# from blog import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('admin/', admin.site.urls),
#     path('', views.Blog_list, name='blog_list'),  # Blog list view
#     path('api/register/', views.RegisterView.as_view(), name='register'),
#     path('api/login/', auth_views.LoginView.as_view(), name='login'),
#     path('create/', views.create_blog, name='create_blog'),  # Create blog post view
#     path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),  # Delete blog post view
#     path('<int:pk>/', views.view_blog, name='view_blog'),  # Single blog post view
#     path('register/', views.register, name='register'),  # User registration view
#     path('login/', auth_views.LoginView.as_view(), name='login'),  # Login view
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
#     path('edit_blog/<int:pk>/', views.edit_blog, name='edit_blog'),  # Added Edit URL
#     path('delete_blog/<int:pk>/', views.delete_blog, name='delete_blog'),
#     path('accounts/profile/', views.profile, name='profile'),
#     path('blog/', include('blog.urls')),  # Ensure blog URLs are included
#     path('', include('blog.urls')), 
#     path('api/blog-posts/', views.BlogPostList.as_view(), name='blog-posts-list'),  # To get the list of blog posts
#     path('api/blog-posts/<int:pk>/', views.BlogPostDetail.as_view(), name='blog-post-detail'),  # To get details of a specific blog post

# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path('', views.home, name='home'),  # Home route (if needed)
    path('admin/', admin.site.urls),  # Admin route
    path('blog/', include('blog.urls')),  # Include blog URLs (app-level routing)


    path('api/register/', views.RegisterAPIView.as_view(), name='register'),  # Registration API
    path('api/blog-posts/', views.BlogPostList.as_view(), name='blog-posts-list'),  # Blog posts list (API)
    path('api/blog-posts/<int:pk>/', views.BlogPostDetail.as_view(), name='blog-post-detail'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='profile_api'),
    path('api/blog-posts/<int:pk>/edit/', views.edit_blog, name='edit_blog'),
    path('api/blog-posts/<int:pk>/delete/', views.delete_blog, name='delete_blog_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Media URL handling for development