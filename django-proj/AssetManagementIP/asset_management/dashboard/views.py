from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from authz.models import User
from django.db.models import Q
from my_assets.models import Asset
from employee_side.models import AssetRequest

# Create your views here.


@login_required
def dashboard(request):
    if request.user in User.objects.filter(groups__name='Employee'):
        return render(request, 'acquired_assets.html')
    elif request.user in User.objects.filter(groups__name='HR'):
        return redirect(reverse("hr_side:asset-requests"))
    elif request.user in User.objects.filter(groups__name='Organization Admin'):
        number_of_assets = len(Asset.objects.filter(
            organization=request.user.from_organization))
        if number_of_assets == 0:
            in_use = 0
        else:
            in_use = round((len(Asset.objects.filter(
                Q(organization=request.user.from_organization) & Q(
                    status=Asset.IN_USE)
            )
            )/number_of_assets)*100, 2)
        needs_maintenance = len(Asset.objects.filter(
            Q(organization=request.user.from_organization) & Q(
                status=Asset.NEED_MAINTENANCE)
        )
        )
        pending = len(AssetRequest.objects.filter(Q(
            status=AssetRequest.PENDING) | Q(status=AssetRequest.APPROVED)))
        context = {
            'number_of_assets': number_of_assets,
            'in_use': in_use,
            'needs_maintenance': needs_maintenance,
            'pending': pending
        }
        return render(request, 'dashboard_home.html', context=context)
