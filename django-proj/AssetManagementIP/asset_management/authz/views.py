# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views import View
from django.contrib.auth.models import auth, User, Group
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from authz.models import Organization

# Login class view


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):

        email = request.POST['email']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email.lower()).username
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                # print("logged in ")
                if request.GET.get('next', "") != "":
                    return redirect(request.GET['next'])
                return redirect(reverse('dashboard:homepage'))
            else:
                messages.info(request, "invalid credentials")
                return redirect(reverse('login'))

        except ObjectDoesNotExist as ex:
            print(ex.__class__)
            messages.error(request, "user does not exists")
            return redirect(reverse('login'))

        except Exception as ex:
            return HttpResponse(ex.__class__.__name__, 500)


class Register(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password0 = request.POST['password0']
        password1 = request.POST['password1']

        username = request.POST['username'].lower()
        if User.objects.filter(username=username).exists():
            messages.info(request,
                          'Username is taken',
                          extra_tags='safe')
            return redirect(reverse('register'))
        if password0 == password1:
            # print(Organization.objects.values_list('email_domain', flat=True))
            if email.split("@")[1] in Organization.objects.values_list('email_domain', flat=True):
                # it has to be a registered organization's email with membership
                if Organization.objects.get(email_domain=email.split("@")[1]).membership:
                    if User.objects.filter(email=email).exists():
                        messages.info(request,
                                      'You are already registered, Please <a href="/login" style="color: blue;">Log In</a>',
                                      extra_tags='safe')
                        return redirect(reverse('register'))
                    else:  # if user is new

                        user = User.objects.create_user(
                            username=username,
                            password=password0,
                            email=email,
                            first_name=firstname,
                            last_name=lastname
                        )
                        employeeGroup = Group.objects.get(
                            name='Employee')
                        employeeGroup.user_set.add(user)
                        user.save()
                        auth.login(request, user)
                        messages.info(request, "Welcome " + firstname + "!")
                        return redirect(reverse('dashboard:homepage'))
                else:
                    messages.info(
                        request, "Sorry, your membership is expired!")
                    return redirect(reverse('register'))
            else:
                messages.info(
                    request, "Sorry, your orgnization does not have a membership")
                return redirect(reverse('register'))

# logout view


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))
