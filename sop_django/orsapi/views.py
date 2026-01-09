from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .ctl.DoctorCtl import DoctorCtl
from .ctl.RoleCtl import RoleCtl

# Create your views here.
@csrf_exempt
def action(request, page, action="get", id=0, pageNo=1):
    methodCall = page + "Ctl()." + action + "(request,{'id':id, 'pageNo':pageNo})"
    response = eval(methodCall)
    return response