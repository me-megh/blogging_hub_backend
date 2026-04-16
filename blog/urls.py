# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.Blog_list, name='Blog_list'),
#     path('create/', views.create_blog, name='create_blog'),
#     path('update/<int:pk>/', views.update_blog, name='update_blog'),
#     path('delete/<int:pk>/', views.delete_blog, name='delete_blog'),
#     path('view/<int:pk>/', views.view_blog, name='view_blog'),
#     path('', views.home, name='home'),
#     path('csrf-token/', views.csrf_token_view, name='csrf_token'),
    
# ]

# blog/urls.py (App-level URL routing)
from django.urls import path
from . import views
from .views import LoginAPIView,csrf_token_view,custom_login,RegisterAPIView,LogoutAPIView,CreateBlogView,delete_blog,edit_blog



urlpatterns = [
    # Blog post routes (for web views)
    path('', views.Blog_list, name='blog_list'),  # Blog list view
    path('create/', CreateBlogView.as_view(), name='create_blog_api') , # Create blog post view
    path('update/<int:pk>/', views.update_blog, name='update_blog'),  # Update blog post view
    path('api/blog/<int:pk>/delete/', views.delete_blog, name='delete_blog_api'),# Delete blog post view
    path('view/<int:pk>/', views.view_blog, name='view_blog'),  # Single blog post view
   path('api/blog/<int:pk>/edit/', views.edit_blog, name='edit_blog'),
    path('api/blog/<int:pk>/update/', views.update_blog, name='update_blog'),
    path('api/login/', custom_login, name='login'), 
    
    path('blog/api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='profile_api'),
    path('api/register/', RegisterAPIView.as_view(), name='register'), 
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),

    # CSRF token route (for API use or Ajax requests)
    path('csrf-token/', csrf_token_view, name='csrf_token'),
]