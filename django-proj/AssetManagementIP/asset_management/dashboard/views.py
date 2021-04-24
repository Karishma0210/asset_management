from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q
# Create your views here.


@login_required
def dashboard(request):
    if request.user in User.objects.filter(Q(groups__name='HR') | Q(groups__name='Organization Admin')):
        return render(request, 'dashboard_home.html')
    else:
        return render(request, 'employee_dashboard.html')
