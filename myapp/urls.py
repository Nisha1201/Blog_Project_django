from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('update/',views.update,name='update'),
    path('profile/',views.profile,name='profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('login/', views.user_login, name='login'),
    path('signup/',views.signup, name="signup"),
    path('logout/', views.user_logout, name='logout'),
    path('like/<int:id>/', views.like_post, name='like_post'),
    path('dislike/<int:id>/',views.dislike_post,name='dislike_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
