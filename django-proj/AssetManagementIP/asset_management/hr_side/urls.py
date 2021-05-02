from django.urls import path
from . import views

app_name = 'hr_side'
urlpatterns = [
    # path('', views.requests, name='asset-requests'),
    path('', views.requests, name='asset-requests'),
    path('previous', views.previousRequests, name='asset-pre-requests'),
    path('<int:request_id>',
         views.ApproveRequestAsset.as_view(), name='approve-request'),
    # path('request-confirm', views.rqSubmitted, name='rqSubmitted'),
]
