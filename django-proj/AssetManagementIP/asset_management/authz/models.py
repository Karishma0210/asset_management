from django.db import models
import datetime
# Create your models here.
# it has to be assosiated with Task


class Organization(models.Model):
    name = models.CharField(max_length=127)
    website = models.CharField(max_length=127)
    email_domain = models.CharField(max_length=127)
    membership = models.BooleanField(default=False)
    membership_start_date = models.DateField(default=datetime.date.today)
    membership_end_date = models.DateField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "orgnization"
