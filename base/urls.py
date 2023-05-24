from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('profile/<int:pk>/', views.userProfile, name='profile'),
    path('update-profile/<int:pk>/', views.updateProfile, name='update-profile'),
    path('create-room/', views.createRoom, name='create-room'),
    path('view-room/<int:pk>/', views.viewRoom, name='view-room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete-message'),
    path('topics', views.topicPage, name='topics'),
    path('activity', views.activityPage, name='activity')
]
