"""ResManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from editorDB import views

urlpatterns = [
    url(r'^editorDB/index', views.index, name='index'),
    url(r'^editorDB/task/addtask', views.addtask, name='addtask'),
    url(r'^editorDB/task/(?P<tid>\d+)/savetask', views.savetask, name='savetask'),
    url(r'^editorDB/task/deletetask', views.deletetask, name='deletetask'),
    url(r'^editorDB/task/edittask', views.edittask, name='edittask'),
    url(r'^editorDB/task', views.task, name='task'),
    url(r'^editorDB/machine/addmachine', views.addmachine, name='addmachine'),
    url(r'^editorDB/machine/(?P<mid>\d+)/savemachine', views.savemachine, name='savemachine'),
    url(r'^editorDB/machine/deletemachine', views.deletemachine, name='deletemachine'),
    url(r'^editorDB/machine/editmachine', views.editmachine, name='editmachine'),
    url(r'^editorDB/machine', views.machine, name='machine'),
    url(r'^editorDB/option/addoption', views.addoption, name='addoption'),
    url(r'^editorDB/option/(?P<oid>\d+)/saveoption', views.saveoption, name='saveoption'),
    url(r'^editorDB/option/deleteoption', views.deleteoption, name='deleteoption'),
    url(r'^editorDB/option/editoption', views.editoption, name='editoption'),
    url(r'^editorDB/option', views.option, name='option'),
    url(r'^editorDB/launch/(?P<tid>\d+)/showoptions', views.showoptions, name='showoptions'),
    url(r'^editorDB/launch/addlaunch', views.addlaunch, name='addlaunch'),
    url(r'^editorDB/launch/(?P<lid>\d+)/savelaunch', views.savelaunch, name='savelaunch'),
    url(r'^editorDB/launch/deletelaunch', views.deletelaunch, name='deletelaunch'),
    url(r'^editorDB/launch/editlaunch', views.editlaunch, name='editlaunch'),
    url(r'^editorDB/launch', views.launch, name='launch'),
    #url(r'^editorDB/lauopt/addlauopt', views.addlauopt, name='addlauopt'),
    url(r'^editorDB/lauopt/(?P<loid>\d+)/savelauopt', views.savelauopt, name='savelauopt'),
    #url(r'^editorDB/lauopt/deletelauopt', views.deletelauopt, name='deletelauopt'),
    url(r'^editorDB/lauopt/editlauopt', views.editlauopt, name='editlauopt'),
    url(r'^editorDB/lauopt', views.lauopt, name='lauopt'),
    url(r'^editorDB/forecasting/funcresult', views.funcresult, name='funcresult'),
    url(r'^editorDB/forecasting', views.forecasting, name='forecasting'),
    url(r'^admin/', include(admin.site.urls)),
]
