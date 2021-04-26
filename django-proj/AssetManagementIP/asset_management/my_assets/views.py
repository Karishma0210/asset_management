from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Asset
from .forms import AssetCreateForm
from authz.models import User
# Create your views here.


@login_required
def assets(request):
    if request.user in User.objects.filter(groups__name='Organization Admin'):
        context = {
            'assets': Asset.objects.all()
        }
        return render(request, 'all_assets.html', context=context)
    else:
        return redirect(reverse('dashboard:homepage'))


@method_decorator(login_required, name="dispatch")
class CreateAsset(View):
    def get(self, request):
        form = AssetCreateForm()
        context = {
            'form': form
        }
        return render(request, "create_asset_form.html", context=context)

    def post(self, request):
        form = AssetCreateForm(request.POST)
        if form.is_valid():
            org_code = request.user.from_organization.organization_code
            last_asset = Asset.objects.filter(
                relative_id__startswith=org_code).order_by('-registration_date')
            asset = form.save(commit=False)
            if len(last_asset) > 0:
                next_number = str(int(last_asset[0].relative_id[3:]) + 1)[-5:]
            else:
                next_number = '00001'
            asset.relative_id = org_code + next_number
            asset.save()
            return redirect(reverse('my_assets:show-qr', kwargs={'asset_rID': "MDX00001"}))

        return HttpResponse("asset added, yet to be developed post")
        # return HttpResponse(ex.__class__.__name__, 500)


def showQR(request, asset_rID):
    context = {
        'code': asset_rID
    }
    return render(request, 'show_qr_code.html', context=context)
