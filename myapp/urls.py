from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage_view, name='landingpage'),
    path('sign-in/', views.signin_view, name='sign-in'),
    path('sign-up/', views.signup_view, name='sign-up'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('reception/', views.reception_list, name='reception'),
    path('profile/', views.profile_view, name='profile'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('admin_profile/', views.admin_profile_view, name='admin_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('save_date/', views.save_date_view, name='save_date'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_page, name='success'),
    path('welcome/', views.welcome_page, name='welcome'),
    path('welcome/details/', views.details_page, name='details'),
    path('reception/<int:id>/', views.animal_detail, name='animal_detail'),
    path('save_image/', views.save_image, name='save_image'),
    path('delete_animal/<int:animal_id>/', views.delete_animal, name='delete_animal'),
    path('profile/<int:submission_id>/', views.client_form_detail, name='client_form_detail'),
    path('delete_account/<int:user_id>/', views.delete_account, name='delete_account'),
    path('remove_from_blacklist/<str:email>/', views.remove_from_blacklist, name='remove_from_blacklist'),
    path('login/help', views.help_view, name='help_view'),
]
