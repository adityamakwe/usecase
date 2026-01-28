import json

from django.http import HttpResponse, JsonResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Course
from ..service.CourseService import CourseService


class CourseCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id')
        self.form['name'] = requestForm.get('name')
        self.form['description'] = requestForm.get('description')
        self.form['duration'] = requestForm.get('duration')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.duration = self.form['duration']
        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['description'] = obj.description
        self.form['duration'] = obj.duration

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Course Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Course Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Course Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['duration'])):
            inputError['duration'] = "Course Duration can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            course = self.get_service().get(params['id'])
            self.model_to_form(course)
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {"result": {}, "success": True}
        if (self.input_validation()):
            res["success"] = False
            res["result"]["inputerror"] = self.form["inputError"]
        else:
            if params['id'] > 0:
                pk = params['id']
                duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Course Name already exists"
                else:
                    r = self.form_to_model(Course())
                    self.get_service().save(r)
                    self.form['id'] = r.id
                    res["success"] = True
                    res["result"]["message"] = "Course updated successfully"
                return JsonResponse(res)
            else:
                duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Course Name already exists"
                else:
                    course = self.form_to_model(Course())
                    self.get_service().save(course)
                    res["success"] = True
                    res["result"]["message"] = "Course added successfully"
        return JsonResponse(res)

    def search(self, request, params={}):
        json_request = json.loads(request.body)
        res = {"result": {}, "success": True}
        if (json_request):
            params["name"] = json_request.get("name", None)
            params["pageNo"] = json_request.get("pageNo", None)
        records = self.get_service().search(params)
        if records and records.get("data"):
            res["success"] = True
            res["result"]["data"] = records["data"]
            res["result"]["lastId"] = Course.objects.last().id
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

    def get_service(self):
        return CourseService()
