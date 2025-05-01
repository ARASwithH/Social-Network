from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('registration', views.UserRegistration.as_view(), name='registration'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('page/<int:user_id>/', views.UserPage.as_view(), name='page'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='unfollow'),
    path('profile/detail/<int:user_id>/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile/detail/update/<int:user_id>/', views.UserProfileDetailUpdateView.as_view(), name='profile_update'),

]
