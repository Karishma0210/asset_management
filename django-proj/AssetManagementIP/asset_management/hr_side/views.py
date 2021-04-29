from django.shortcuts import render, redirect, reverse
from my_assets.models import Category, Asset
from authz.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from .models import AssetRequest
# Create your views here.


@login_required
def requests(request):
    hr = request.user
    assetReqs = AssetRequest.objects.filter(request_to=hr)

    context = {
        'assetReqs': assetReqs
    }
    return render(request, "asset_rqs_hr.html", context=context)


@method_decorator(login_required, name="dispatch")
class ApproveRequestAsset(View):
    def get(self, request, request_id):
        hr = request.user
        assetReq = AssetRequest.objects.get(id=request_id)

        context = {
            'assetReq': assetReq
        }
        return render(request, "approve_rq_hr.html", context=context)

    def post(self, request):
        print("recorded")
        return redirect(reverse("hr_side:approve-request"))
