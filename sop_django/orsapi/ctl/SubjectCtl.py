import json

from django.http import JsonResponse
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from ..models import Subject
from ..service.SubjectService import SubjectService
from ..service.CourseService import CourseService


class SubjectCtl(BaseCtl):

    # def preload(self, request, params={}):
    #     self.dynamic_preload = CourseService().preload()

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['name'] = requestForm.get('name','')
        self.form['description'] = requestForm.get('description','')
        self.form['courseId'] = requestForm.get('courseId','')
        if self.form['courseId'] != '':
            course = CourseService().get(self.form['courseId'])
            self.form["courseName"] = course.name

    def form_to_model(self, obj):
        course = CourseService().get(self.form['courseId'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.courseId = self.form['courseId']
        obj.courseName = course.name
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['description'] = obj.description
        self.form['courseId'] = obj.courseId
        self.form['courseName'] = obj.courseName

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Subject Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Subject Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['courseId'])):
            inputError['courseId'] = "Course can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            id = params['id']
            subject = self.get_service().get(id)
            self.model_to_form(subject)
        res = render(request, self.get_template(), {'form': self.form, 'courseList': self.dynamic_preload})
        return res

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {"result": {}, "success": True}
        if (self.input_validation()):
            res["success"] = False
            res["result"]["inputerror"] = self.form["inputError"]
        else:
            if (params['id'] > 0):
                pk = params['id']
                duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Subject Name already exists"
                else:
                    subject = self.form_to_model(Subject())
                    self.get_service().save(subject)
                    self.form['id'] = subject.id
                    res["success"] = True
                    res["result"]["message"] = "Subject updated successfully"
            else:
                duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Subject Name already exists"
                else:
                    subject = self.form_to_model(Subject())
                    self.get_service().save(subject)
                    res["success"] = True
                    res["result"]["message"] = "Subject added successfully"
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
            res["result"]["lastId"] = Subject.objects.last().id
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def get(self, request, params={}):
        subject = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (subject != None):
            res["success"] = True
            res["result"]["data"] = subject.to_json()
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def delete(self, request, params={}):
        subject = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (subject != None):
            self.get_service().delete(params["id"])
            res["success"] = True
            res["result"]["data"] = subject.to_json()
            res["result"]["message"] = "Data has been deleted successfully"
        else:
            res["success"] = False
            res["result"]["message"] = "Data was not deleted"
        return JsonResponse(res)

    def preload(self, request, params={}):
        res = {"result": {}, "success": True}
        course_list = CourseService().preload()
        preloadList = []
        for x in course_list:
            preloadList.append(x.to_json())
        res["result"]["courseList"] = preloadList
        return JsonResponse(res)

    def get_service(self):
        return SubjectService()
