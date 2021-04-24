from django.urls import path
from . import views

app_name = 'my_assets'
urlpatterns = [
    path('', views.assets, name='assets'),
    path('add-assets', views.AddAsset.as_view(), name='add-asset'),
]
