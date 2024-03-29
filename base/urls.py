from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [ 
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('sign-up', views.register, name='register'),


    path('', views.home, name='home'),
    path('create-rooms', views.create_room, name='create_rooms'),
    path('update-room/<int:pk>', views.update_room, name='update_room'),
    path('delete-room/<int:pk>', views.delete_room, name='delete_room'),
    path('create-room', views.create_room, name='create_room'),


    path('room/<int:pk>', views.room, name='room'),


    path('user-profile/<int:pk>', views.user_profile, name='user_profile'),
    path('edit-profile/<int:pk>', views.edit_profile, name='edit_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)