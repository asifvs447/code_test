from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .api_views import *
from .views import *

urlpatterns = [
    # home page
    url(r'^$', HomelyAppIndex.homepage, name='index'),

    # register, login and logout views
    url(r'^register/$', Register.register, name='register'),
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # list all prop
    url(r'^properties_list/$', AllAvailProperties.allavailprop, name='propertieslist'),

    # user profile/add/update/delete properties
    url(r'^accounts/profile/$',TemplateView.as_view(template_name='profile.html'), name='userprofile'),
    url(r'^accounts/profile/addproperty/$',AddProperties.addproperty, name='useraddproperty'),
    url(r'^accounts/profile/show_listed/$',PropertiesList.listproperties, name='userlisted'),
    url(r'^accounts/profile/show_listed/edit/(?P<pk>[0-9]+)/$',UpdateProperty.as_view(), name='editproperty'),
    url(r'^accounts/profile/show_listed/(?P<pk>[0-9]+)/delete/$',DeleteProperty.as_view(), name='deleteproperty'),

    # tenant
    url(r'^properties_list/(?P<pk>[0-9]+)/rent/$',RentProperty.rent_property, name='rentproperty'),
    url(r'^accounts/profile/tenant_property_list/$',TenantProperties.tenantproperties, name='tenantproperty'),



    url(r'^renter_notallowed/$',AddProperties.addproperty, name='useraddproperty'),


    # API views
    url(r'^api/login/$', LoginView.as_view(), name='apilogin'),
    url(r'^api/create_user/$', UserCreate.as_view(), name='apicraeteuser'),
    url(r'^api/users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]