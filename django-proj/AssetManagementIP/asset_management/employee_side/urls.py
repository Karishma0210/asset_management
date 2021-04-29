from django.urls import path
from . import views

app_name = 'employee_side'
urlpatterns = [
    path('', views.acquiredAssets, name='acquired-assets'),
    path('request-asset', views.RequestAsset.as_view(), name='request-asset'),
    path('request-confirm', views.rqSubmitted, name='rqSubmitted'),
]
