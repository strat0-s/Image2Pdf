from django.urls import path
from .views import register, login_view, logout_view

urlpatterns = [
    path('register/', register, name='register1'),
    path('login/', login_view, name='login1'),
    path('logout/', logout_view, name='logout1'),
]
