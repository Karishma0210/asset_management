from django.db import models
from django.conf import settings
# Create your models here.


class AssetRequest(models.Model):
    asset_description = models.CharField(max_length=127)
    organization = models.ForeignKey('authz.Organization',
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True)

    asset = models.ForeignKey('my_assets.Asset', on_delete=models.CASCADE,
                              blank=True, null=True)
    category = models.ForeignKey('my_assets.Category',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    requirement_date = models.DateField()
    returning_date = models.DateField()

    rq_msg = models.TextField(max_length=200, blank=True,
                              null=True)  # for any comments
    request_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE)

    request_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='%(class)s_request_to')

    def __str__(self):
        return self.asset_description + "from: " + self.user + ", to:" + self.request_to
