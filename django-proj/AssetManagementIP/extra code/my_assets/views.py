from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
# Create your views here.


@method_decorator(login_required, name="dispatch")
class MyAssets(View):
    def get(self, request):
        return HttpResponse("my assets page to be contructed")
        # return render(request, 'dashboard.html')

    def post(self, request):
        try:
            return HttpResponse("post request in my assets is still under contruction")

        except Exception as ex:
            return HttpResponse(ex.__class__.__name__, 500)


@method_decorator(login_required, name="dispatch")
class AddAssets(View):
    def get(self, request):
        return HttpResponse("add assets page to be contructed")
        # return render(request, 'dashboard.html')

    def post(self, request):
        try:
            return HttpResponse("post request in my assets is still under contruction")

        except Exception as ex:
            return HttpResponse(ex.__class__.__name__, 500)
