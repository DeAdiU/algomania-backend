from django.urls import path,include
from .views import SignupView, LoginView, get_profile, UserViewSet, get_recent_submissions, push_submissions, ProfQuesViewSet,TeamViewSet, update_team_id,get_teams,  get_top,user_detail, all_teams_summary
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'submissions', UserViewSet, basename='submissions')
router.register(r'prof_questions', ProfQuesViewSet, basename='prof_questions')
router.register(r'teams', TeamViewSet, basename='team')


urlpatterns = [
    path('register/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('get_profile/', get_profile, name='get_profile'),
    path('get_recent_submissions/', get_recent_submissions, name='get_submissions'),
    path('push_submissions/', push_submissions, name='push_submissions'),
    path('set_team_id/', update_team_id, name='set_team_id'),
    path('get_team/', get_teams, name='get_team'),
    path('',include(router.urls)),
    path('user_detail/', user_detail, name='user_detail'),
    path('get_top_team_user/', get_top, name='get_dashboard'),
    path('all_teams_summary/', all_teams_summary, name='all_teams_summary'),
]