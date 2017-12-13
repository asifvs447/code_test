from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from .models import UserProfiles, RentoutProperties, Renter
from .forms import UserForm, UserProfileForm, RentoutPropertyForm
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


class HomelyAppIndex(object):
    def homepage(request):
        return render(request, 'index.html')


class Register(object):
    def register(request):
        uf = UserForm(request.POST, prefix='user')
        upf = UserProfileForm(request.POST, prefix='userprofile')
        if request.method == 'POST':
            uf = UserForm(request.POST, prefix='user')
            upf = UserProfileForm(request.POST, prefix='userprofile')
            if uf.is_valid() * upf.is_valid():
                user = uf.save()
                user.set_password(user.password)
                user.save()
                userprofile = upf.save(commit=False)
                userprofile.user = user
                userprofile.save()
                return HttpResponseRedirect('/accounts/profile')
            else:
                uf = UserForm(prefix='user')
                upf = UserProfileForm(prefix='userprofile')
        return render(request, 'register.html', dict(userform=uf,userprofileform=upf), RequestContext(request))

# list all prop by all users
class AllAvailProperties(ListView):
    def allavailprop(request):
        if request.user.username is None or request.user.username =='':
            return HttpResponseRedirect('/login/')
        else:
            all_properties = RentoutProperties.objects.filter(house_rented=False)
            all_properties = all_properties.values()
            return render(request, 'rentoutproperties.html', {'all_properties': all_properties})


#list all properties by all logged in user
class PropertiesList(ListView):
    def listproperties(request):
        dbuser = User.objects.get(username=request.user.username)
        db_owned_properties = RentoutProperties.objects.filter(house_owner=dbuser)
        return render(request,'listproperties.html', {'list_houses':db_owned_properties})


#add new prop
class AddProperties(object):
    def addproperty(request):
        if request.user.username is None or request.user.username == '':
            return HttpResponseRedirect('/login/')
        db_user_id=request.user.id
        user_profile = UserProfiles.objects.get(user=db_user_id)
        if user_profile.account_type == 1:
            return HttpResponseRedirect('/renter_notallowed/')
        elif user_profile.account_type == 0:
            addpropform = RentoutPropertyForm(request.POST, initial={'user': db_user_id},prefix='addpropform')
            if addpropform.is_valid():
                addproperty = addpropform.save(commit=False)
                addproperty.house_owner=request.user
                addproperty.save()
                return HttpResponseRedirect('/accounts/profile/show_listed')
            else:
                addpropform = RentoutPropertyForm(request.POST, prefix='addpropform')
        return render(request,'addproperties.html',dict(addpropform=addpropform), RequestContext(request))


#update property
class UpdateProperty(UpdateView):
    model= RentoutProperties
    fields = ['house_name','house_address']


#delete
class DeleteProperty(DeleteView):
    model = RentoutProperties
    success_url= reverse_lazy('homelyapp:userlisted')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# to be able to rent
class RentProperty(object):
    def rent_property(request,pk):
        db_user_id = request.user.id
        user_profile = UserProfiles.objects.get(user=db_user_id)
        if user_profile.account_type == 1:
            current_house=RentoutProperties.objects.get(id=pk)
            current_house.house_rented= True
            renter_obj=Renter(tenant=user_profile.user,house_rented=current_house)
            renter_obj.save()
            current_house.save()
            return render(request,'rentedsucess.html')


# all sucessfull rent of a user
class TenantProperties(object):
    def tenantproperties(request):
        db_user_id = request.user.id
        if request.user.username is None or request.user.username == '':
            return HttpResponseRedirect('/login/')
        user_profile = UserProfiles.objects.get(user=db_user_id)
        if user_profile.account_type == 1:
            all_rented = Renter.objects.filter(tenant=db_user_id)
            return render(request,'rentedsucess.html',{'rented_properties':all_rented})





