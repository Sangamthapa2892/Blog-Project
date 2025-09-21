from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
urlpatterns = [
    # landing page
    path('', views.home, name='home'),
    # login and register4
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
 
    path('blog/', views.blog, name='blog_list'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    path('myblog/', views.mypost, name='mypost'),
    path('blog/edit/<slug:slug>/', views.edit_blog, name='edit_blog'),
    path('blog/delete/<slug:slug>/', views.delete_blog, name='delete_blog'),
    
    # comments
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contact'),
    
    path('password_change/', PasswordResetView.as_view(template_name='user/password_change.html'), name='password_change'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='user/password_change_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='user/password_change_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='user/password_change_complete.html'), name='password_reset_complete'),
]