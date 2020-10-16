from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('create_quote', views.create_quote),
    path('delete_quote/<int:quote_id>', views.delete_quote),
    path('user_quotes/<int:user_id>', views.user_quotes),
    path('edit_account/<int:user_id>', views.edit_account),
    path('edit_account_process/<int:edit_user_id>', views.edit_account_process),
    path('like/<int:quote_id>/<int:user_id>', views.like)
]
