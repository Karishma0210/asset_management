from django.urls import path
from . import views

app_name = 'my_assets'
urlpatterns = [
    path('', views.MyAssets.as_view(), name='my_assets'),
    path('add-assets', views.AddAssets.as_view(), name='add_assets')
]
