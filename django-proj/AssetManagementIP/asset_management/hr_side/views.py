from django.shortcuts import render, redirect, reverse, HttpResponse
from my_assets.models import Category, Asset
from authz.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from employee_side.models import AssetRequest
# Create your views here.


@login_required
def requests(request):
    hr = request.user.id
    # print(hr)
    assetReqs = AssetRequest.objects.filter(
        request_to_id=hr, status=AssetRequest.PENDING)
    # print(assetReqs)
    context = {
        'assetReqs': assetReqs
    }
    return render(request, "asset_rqs_hr.html", context=context)


@method_decorator(login_required, name="dispatch")
class ApproveRequestAsset(View):
    def get(self, request, request_id):
        return HttpResponse("not allowed to view")

    def post(self, request, request_id):
        # print("recorded " + str(request_id))
        try:
            assetReq = AssetRequest.objects.get(id=request_id)
            submitter_btn = request.POST.get("submitter_btn")
            if submitter_btn == "approve_btn":
                assetReq.status = assetReq.APPROVED
                assetReq.save()

            elif submitter_btn == "reject_btn":
                assetReq.status = assetReq.DENIED
                assetReq.save()
            return HttpResponse("Request marked as - {}".format(assetReq.status), 200)
        except ObjectDoesNotExist:
            return HttpResponse("Asset Request does not exists", 404)


@login_required
def previousRequests(request):
    hr = request.user.id
    # print(hr)
    assetReqs = AssetRequest.objects.filter(
        Q(request_to_id=hr) & ~Q(status=AssetRequest.PENDING))
    # print(assetReqs)
    context = {
        'assetReqs': assetReqs
    }
    return render(request, "asset_rqs_hr.html", context=context)
