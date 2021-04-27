from django.urls import path
from . import views

app_name = 'my_assets'
urlpatterns = [
    path('', views.assets, name='assets'),
    path('add-asset', views.CreateAsset.as_view(), name='add-asset'),
    path('import-assets', views.ImportAssets.as_view(), name='import-assets'),
    path('<str:asset_rID>', views.showAsset, name='show-asset')
]
