from django.urls import path
from . import views

app_name = 'my_assets'
urlpatterns = [
    path('', views.assets, name='assets'),
    path('add-asset', views.CreateAsset.as_view(), name='add-asset'),
    path('<str:asset_rID>', views.showQR, name='show-qr'),
]
