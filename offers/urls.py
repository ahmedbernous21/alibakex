from django.urls import path
from offers import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('<int:id>', views.detail, name="detail"),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('customer/<str:pk>/', views.Customer, name="customer"),
    path('welcome', views.welcome, name="welcome"),
    path('CustomerInfo/<str:pk>/', views.CustomerInfo, name="CustomerInfo"),
    path('', views.register, name="register"),
    path('login', views.loginPage, name="login"),
    path('logout', views.LogoutUser, name="logout"),
    path('settings', views.accountSettings, name="settings"),
    path('my_offers', views.my_offers, name="my_offers"),
    path('auth',views.auth, name="auth"),
    path('OffersPage', views.ahmed, name="OffersPage"),
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="offers/password_reset.html"),
    name="reset_password"),
    path('submit', views.submitted, name="submit"),
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="offers/password_reset_sent.html"),
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="offers/password_reset_form.html"),
    name="password_reset_confirm"),

    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="offers/password_reset_done.html"),
    name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)