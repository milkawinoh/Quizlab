from django.urls import path
from .views import register, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', register, name='signup'),
    ]