import json

from django.http import JsonResponse
from django.shortcuts import render
from .BaseCtl import BaseCtl
from ..utility.DataValidator import DataValidator
from ..models import Role
from ..service.RoleService import RoleService


class RoleCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['name'] = requestForm.get('name','')
        self.form['description'] = requestForm.get('description','')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Role Name is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Role Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Description is required"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            role = self.get_service().get(params['id'])
            self.model_to_form(role)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {"result": {}, "success": True}
        if (self.input_validation()):
            res["success"] = False
            res["result"]["inputerror"] = self.form["inputError"]
        else:
            if (int(self.form['id']) > 0):
                pk = int(self.form['id'])
                duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]['message'] = "Role already exist"
                else:
                    role = self.form_to_model(Role())
                    self.get_service().save(role)
                    res['id'] = role.id
                    res['success'] = True
                    res["result"]['message'] = "Role updated successfully"
            else:
                duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
                if duplicate.count() > 0:
                    res['success'] = False
                    res["result"]['message'] = "Role already exist"
                else:
                    role = self.form_to_model(Role())
                    self.get_service().save(role)
                    res['success'] = True
                    res["result"]['message'] = "Role added successfully..!!"
        return JsonResponse(res)

    def search(self, request, params={}):
        json_request = json.loads(request.body)
        res = {"result": {}, "success": True}
        if (json_request):
            params["id"] = json_request.get("id", None)
            params["pageNo"] = json_request.get("pageNo", None)
        records = self.get_service().search(params)
        if records and records.get("data"):
            res["success"] = True
            res["result"]["data"] = records["data"]
            res["result"]["lastId"] = Role.objects.last().id
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def get(self, request, params={}):
        role = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (role != None):
            res["success"] = True
            res["result"]["data"] = role.to_json()
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def delete(self, request, params={}):
        role = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (role != None):
            self.get_service().delete(params["id"])
            res["success"] = True
            res["result"]["data"] = role.to_json()
            res["result"]["message"] = "Data has been deleted successfully"
        else:
            res["success"] = False
            res["result"]["message"] = "Data was not deleted"
        return JsonResponse(res)

    def preload(self, request, params={}):
        res = {"result": {}, "success": True}
        role_list = RoleService().preload()
        preloadList = []
        for x in role_list:
            preloadList.append(x.to_json())
        res["result"]["roleList"] = preloadList
        return JsonResponse(res)

    def get_service(self):
        return RoleService()
