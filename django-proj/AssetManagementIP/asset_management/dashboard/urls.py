from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='homepage'),
    # path('login/', views.Login.as_view(), name='login'),
    # path('logout/', views.logout, name='logout')
]
