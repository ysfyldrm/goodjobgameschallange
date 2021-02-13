from django.urls import path
from .leaderboard import userDetailsAPIView, userCreate,  leaderboard, specificLeaderboard, submitScore


urlpatterns = [
    path('leaderboard/', leaderboard.as_view()),
    path('leaderboard/<slug:country>/', specificLeaderboard.as_view()),
    path('user/profile/<uuid:user_id>/', userDetailsAPIView.as_view()),
    path('user/create/', userCreate.as_view()),
    path('score/submit/<uuid:user_id>/', submitScore.as_view())
]