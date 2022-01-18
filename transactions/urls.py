from django.urls import path
from .views.register import RegisterView
from .views.login import LoginView
from .views.logout import LogoutView
from .views.forgot_password import ForgotPasswordView
from .views.password_reset import ResetPasswordView
from .views.verify_email import VerifyEmail
from .views.open_account import CreateAccountView
from .views.account_balance import CreditBalanceView, DebitBalanceView
from .views.admin_view import DeleteView, DeactivateView, ActivateView, AccountListView, AccountDetailView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('email_verify', VerifyEmail.as_view(), name='email_verify'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('open-account', CreateAccountView.as_view(), name='open-account'),
    path('credit/<int:pk>', CreditBalanceView.as_view(), name='credit'),
    path('debit/<int:pk>', DebitBalanceView.as_view(), name='debit'),
    path('delete/<int:pk>', DeleteView.as_view(), name='delete-user'),
    path('deactivation/<int:pk>', DeactivateView.as_view(), name='deactivation'),
    path('activate/<int:pk>', ActivateView.as_view(), name='activate_user'),
    path('Account-view/', AccountListView.as_view(), name='account-view'),
    path('Account-view/<int:pk>', AccountDetailView.as_view(), name='specific-account'),
]
