from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Asset
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
class AddAsset(View):
    def get(self, request):
        return render(request, "add_asset_form.html")

    def post(self, request):
        return HttpResponse("asset added, yet to be developed post")
        # return HttpResponse(ex.__class__.__name__, 500)
