from django.urls import path,include
from .views import SignupView, LoginView, get_profile, UserViewSet, get_submissions, push_submissions, ProfQuesViewSet,TeamViewSet, update_team_id
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'submissions', UserViewSet, basename='submissions')
router.register(r'prof_questions', ProfQuesViewSet, basename='prof_questions')
router.register(r'teams', TeamViewSet, basename='team')


urlpatterns = [
    path('register/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('get_profile/', get_profile, name='get_profile'),
    path('get_submissions/', get_submissions, name='get_submissions'),
    path('push_submissions/', push_submissions, name='push_submissions'),
    path('set_team_id/', update_team_id, name='set_team_id'),
    path('',include(router.urls))
]