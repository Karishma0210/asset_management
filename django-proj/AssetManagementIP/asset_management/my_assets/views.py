from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from .models import Asset, AssestsFile, Category, Manufacturer, QRCodeImage
from .forms import AssetCreateForm
from django.conf import settings
from authz.models import User
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import csv
import datetime
import traceback
# Create your views here.


@login_required
def assets(request):
    if request.user in User.objects.filter(groups__name='Organization Admin'):
        organization = request.user.from_organization
        print(organization)
        context = {
            'assets': Asset.objects.filter(organization=organization)
        }
        print(context['assets'])
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
            organization = request.user.from_organization
            org_code = organization.organization_code
            last_asset = Asset.objects.filter(
                relative_id__startswith=org_code).order_by('-registration_date')
            asset = form.save(commit=False)
            if len(last_asset) > 0:
                next_number = format(
                    (int(last_asset[0].relative_id[3:])+1)/100000, '.5f')[-5:]
            else:
                next_number = '00001'
            asset.relative_id = org_code + next_number
            asset.organization = organization
            asset.save()
            asset_qr = QRCodeImage(
                name=request.build_absolute_uri() + asset.relative_id)
            asset_qr.save()
            return redirect(reverse('my_assets:show-qr', kwargs={'asset_rID': "MDX00001"}))

        return HttpResponse("unvalid form")


@method_decorator(login_required, name="dispatch")
class ImportAssets(View):
    def get(self, request):
        return render(request, "import_assets.html")

    def post(self, request):
        # for el in request.FILES:
        #     print("FILE - ", el)
        importFile = request.FILES.get('import-file')
        fields_with_errors = []  # --data line numbers with errors--
        # print("UNDER POST ARRIVED", importFile)
        if importFile != None and importFile.name.endswith('.csv'):
            importFile = AssestsFile(
                importedFile=importFile, user=request.user)
            importFile.save()

            with open(importFile.importedFile.path, 'r') as importedCSV:
                reader = csv.DictReader(importedCSV)
                curr_line_number = 0
                try:
                    for line in reader:
                        curr_line_number += 1
                        # check if assets non blank fields exists
                        # print(line)
                        if line['Asset Name'] != '' and line['Category'] != '' and line['Asset Status'] != '':
                            # print(Category.objects.filter(
                            #     name=line['Category'].lower().title()))
                            category, _is_created_ = Category.objects.get_or_create(
                                name=line['Category'].lower().title())

                            status = line['Asset Status'].lower()
                            isValidStatus = (
                                status == Asset.AVAILABLE or status == Asset.IN_USE or status == Asset.NEED_MAINTENANCE)
                            # print("Is Valid status", isValidStatus)
                            if isValidStatus:
                                # get last orgnizational asset id, add orgnization
                                organization = request.user.from_organization
                                org_code = organization.organization_code
                                last_asset = Asset.objects.filter(
                                    relative_id__startswith=org_code).order_by('-registration_date')
                                # print(last_asset)
                                if len(last_asset) > 0:
                                    # 00002
                                    next_number = format(
                                        (int(last_asset[0].relative_id[3:])+1)/100000, '.5f')[-5:]

                                else:
                                    next_number = '00001'

                                #--------save actual data now-------#
                                # print(category)
                                asset, _is_created_ = Asset.objects.get_or_create(
                                    name=line['Asset Name'].lower().title(),
                                    category=category,
                                    status=status
                                )
                                asset.save()

                                asset.relative_id = org_code + next_number
                                asset.organization = organization
                                asset.manufacturer, _is_created_ = Manufacturer.objects.get_or_create(
                                    name=line['Manufacturer'].lower().title())
                                try:
                                    asset.asset_user = User.objects.get(
                                        email=line['Asset User'])
                                    # print(asset.asset_user)
                                except Exception as ex:
                                    # print(ex.__class__)
                                    print(ex)
                                    fields_with_errors.append(
                                        (curr_line_number, "Asset User"))
                                asset.location = line['Location'].lower(
                                ).title()
                                try:
                                    asset.purchase_date = datetime.datetime.strptime(
                                        line['Purchase Date'], '%d/%m/%Y').date()
                                except Exception as ex:
                                    # print(ex.__class__)
                                    # print(ex)
                                    fields_with_errors.append(
                                        (curr_line_number, "Purchase Date"))
                                try:
                                    asset.warranty = 0 if line['Warranty'] == '' else int(
                                        line['Warranty'])
                                except Exception as ex:
                                    # print(ex.__class__)
                                    # print(ex)
                                    fields_with_errors.append(
                                        (curr_line_number, "Warranty"))
                                try:
                                    asset.last_repair = datetime.datetime.strptime(
                                        line['Last Repair'], '%d/%m/%Y').date()
                                except Exception as ex:
                                    # print(ex.__class__)
                                    # print(ex)
                                    fields_with_errors.append(
                                        (curr_line_number, "Last Repair"))
                                phy_address = line['Physical Address'].lower()
                                phyAddExists = False if len(Asset.objects.filter(
                                    physical_address=phy_address)) == 0 else True
                                if phyAddExists:
                                    asset.physical_address = ''
                                    fields_with_errors.append(
                                        (curr_line_number, "Physical Address"))
                                else:
                                    asset.physical_address = phy_address
                                asset.digital_key = line['Digital Key'].lower()
                                asset.note = line['Comments'].lower(
                                ).capitalize()
                                asset.save()
                                if fields_with_errors:  # non-empty, so has errors
                                    messages.info(
                                        request, "Imported with some missing fields!")
                                else:
                                    messages.info(
                                        request, "CSV file successfully imported!")
                                #---sending variable using session cookie to display errors on frontend---#
                                request.session['error_fields'] = fields_with_errors

                            else:
                                fields_with_errors.append(
                                    (curr_line_number, "Asset Status"))
                                messages.info(
                                    request, "CSV file successfully imported!")
                        else:
                            fields_with_errors.append(
                                (curr_line_number, "all"))
                        asset_qr = QRCodeImage(
                            name=request.build_absolute_uri() + asset.relative_id)
                        asset_qr.save()
                    return redirect(reverse('my_assets:import-assets'))
                except IntegrityError as ex:
                    messages.info(
                        request, "Assets mentioned already exists")
                except OperationalError as ex:
                    messages.info(
                        request, "Database is locked!, try again")
                except Exception as ex:
                    print(ex.__class__)
                    traceback.print_exc()
                    print("MAIN TRY CATCH ERROR")

            importFile.delete()
        return redirect(reverse('my_assets:import-assets'))


def showAsset(request, asset_rID):
    try:
        asset = Asset.objects.get(relative_id=asset_rID)
        qrCodeImg, _is_created_ = QRCodeImage.objects.get_or_create(
            asset=asset, name=request.build_absolute_uri())
        context = {
            'asset': asset,
            'employeeList': getEmployees(request.user.from_organization),
            'adminList': getAdmins(request.user.from_organization),
            'qrCodeImg': qrCodeImg
        }
        return render(request, 'show_asset.html', context=context)
    except ObjectDoesNotExist:
        return HttpResponse("Asset Does not exist", 404)


def getEmployees(org):
    return User.objects.filter(Q(groups__name='Employee') & Q(from_organization=org))


def getHRs(org):
    return User.objects.filter(Q(groups__name='HR') & Q(from_organization=org))


def getAdmins(org):
    return User.objects.filter(Q(groups__name="Organization Admin") & Q(from_organization=org))
