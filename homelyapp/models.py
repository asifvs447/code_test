# django
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# rest framework
from rest_framework.authtoken.models import Token



HOMEOWNER = 0
RENTER = 1
STAFF = 2

USERTYPES = ((HOMEOWNER, 'Home Owner'),(RENTER, 'Renter'), (STAFF, 'Staff'))


class UserProfiles(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    account_type=models.IntegerField(choices=USERTYPES)
    phone = models.IntegerField()

    def __str__(self):
        return self.user.username + self.user.email +  str(self.phone) + str(self. account_type)


class RentoutProperties(models.Model):
    house_owner = models.ForeignKey(User)
    house_name = models.CharField(max_length=30, unique=True)
    house_address = models.CharField(max_length=50, unique=True)
    house_rented = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('homelyapp:userlisted')

    def __str__(self):
        return str(self.house_owner) + self.house_name + self.house_address


class Renter(models.Model):
    tenant = models.ForeignKey(User)
    house_rented = models.ForeignKey(RentoutProperties)

    def __str__(self):
        return str(self.tenant) + '-' + str(self.house_rented)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)