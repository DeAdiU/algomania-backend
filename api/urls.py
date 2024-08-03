from django.urls import path
from .views import SignupView, LoginView, get_profile


urlpatterns = [
    path('register/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('get_profile/', get_profile, name='get_profile'),
]