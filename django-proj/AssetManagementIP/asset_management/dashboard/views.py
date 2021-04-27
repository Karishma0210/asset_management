from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from authz.models import User
from django.db.models import Q


# Create your views here.
@login_required
def dashboard(request):
    if request.user in User.objects.filter(groups__name='Employee'):
        return render(request, 'employee_dashboard.html')
    elif request.user in User.objects.filter(groups__name='HR'):
        return render(request, 'hr_dashboard.html')
    elif request.user in User.objects.filter(groups__name='Organization Admin'):
        return render(request, 'dashboard_home.html')
