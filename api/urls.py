from django.urls import path
from .views import SignupView, LoginView, get_user


urlpatterns = [
    path('register/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('get_profile/', get_user, name='get_profile'),
]