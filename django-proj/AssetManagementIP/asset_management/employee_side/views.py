from django.shortcuts import render, redirect, reverse
from my_assets.models import Category, Asset
from authz.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from .models import AssetRequest


@method_decorator(login_required, name="dispatch")
class RequestAsset(View):
    def get(self, request):
        organization = request.user.from_organization
        categories = Category.objects.filter(
            organization=organization)
        hrs = getHRs(organization)

        context = {
            'categories': categories,
            'hrs': hrs
        }
        return render(request, "request_asset.html", context=context)

    def post(self, request):
        asset_description = request.POST.get("assetDescrip")
        organization = request.user.from_organization
        category = Category.objects.get(id=request.POST.get("category"))

        requirement_date = request.POST.get("rq_date")
        returning_date = request.POST.get("rt_date")
        rq_msg = request.POST.get("rq_msg")
        request_from = request.user
        hr = User.objects.get(id=request.POST.get("hr"))
        assetRequest = AssetRequest.objects.create(
            asset_description=asset_description,
            organization=organization,
            category=category,

            requirement_date=requirement_date,
            returning_date=returning_date,
            rq_msg=rq_msg,
            request_from=request_from,
            request_to=hr
        )
        return redirect(reverse("employee_side:rqSubmitted"))


def acquiredAssets(request):
    context = {
        'assets': Asset.objects.filter(
            Q(organization=request.user.from_organization)
        )
    }
    return render(request, "acquired_assets.html", context=context)


def rqSubmitted(request):
    return render(request, "rq-submitted.html")


def getHRs(org):
    return User.objects.filter(Q(groups__name='HR') & Q(from_organization=org))
