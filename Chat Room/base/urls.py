from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('room/<int:pk>/', room_view, name='room'),

    path('create-room/', create_room_view, name='create_room'),
    path('<int:pk>/update/', update_room_view, name='update_room'),
    path('<int:pk>/delete-room/', delete_room_view, name='delete_room'),
    path('<int:pk>/delete-message/', delete_message_view, name='delete_message'),

    path('user_profile/<int:pk>/', user_profile_view, name='user_profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='register'),

    path('update-user/', user_update_view, name='update_user'),
    path('topics/', topics_view, name='topics'),
]
