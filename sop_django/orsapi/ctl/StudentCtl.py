import json
from django.http import JsonResponse
from ..service.CollegeService import CollegeService
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import Student
from ..service.StudentService import StudentService


class StudentCtl(BaseCtl):

    def preload(self, request, params={}):
        self.dynamic_preload = CollegeService().preload()

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['firstName'] = requestForm.get('firstName','')
        self.form['lastName'] = requestForm.get('lastName','')
        self.form['dob'] = requestForm.get('dob','')
        self.form['mobileNumber'] = requestForm.get('mobileNumber','')
        self.form['email'] = requestForm.get('email','')
        self.form['collegeId'] = requestForm.get('collegeId','')

        if self.form['collegeId'] != '':
            college = CollegeService().get(self.form['collegeId'])
            self.form["collegeName"] = college.name

    def form_to_model(self, obj):
        college = CollegeService().get(self.form['collegeId'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.dob = self.form['dob']
        obj.mobileNumber = self.form['mobileNumber']
        obj.email = self.form['email']
        obj.collegeId = self.form['collegeId']
        obj.collegeName = college.name
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['firstName'] = obj.firstName
        self.form['lastName'] = obj.lastName
        self.form['dob'] = obj.dob.strftime("%Y-%m-%d")
        self.form['mobileNumber'] = obj.mobileNumber
        self.form['email'] = obj.email
        self.form['collegeId'] = obj.collegeId
        self.form['collegeName'] = obj.collegeName

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['firstName'])):
            inputError['firstName'] = "First Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] = "Last Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['lastName'])):
                inputError['lastName'] = "Last Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['dob'])):
            inputError['dob'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['mobileNumber'])):
            inputError['mobileNumber'] = "Mobile Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobileNumber'])):
                inputError['mobileNumber'] = "Mobile Number must start with 6,7,8,9"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['email'])):
            inputError['email'] = "Email can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Email Id must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['collegeId'])):
            inputError['collegeId'] = "College can not be null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            student = self.get_service().get(params['id'])
            self.model_to_form(student)
        res = render(request, self.get_template(), {'form': self.form, 'collegeList': self.dynamic_preload})
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
                duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(email=self.form['email'])
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Email already exists"
                else:
                    student = self.form_to_model(Student())
                    self.get_service().save(student)
                    self.form['id'] = student.id
                    res["success"] = True
                    res["result"]["message"] = "Student updated successfully"
            else:
                duplicate = self.get_service().get_model().objects.filter(email=self.form['email'])
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Email already exists"
                else:
                    student = self.form_to_model(Student())
                    self.get_service().save(student)
                    res["success"] = True
                    res["result"]["message"] = "Student added successfully"
        return JsonResponse(res)

    def search(self, request, params={}):
        json_request = json.loads(request.body)
        res = {"result": {}, "success": True}
        if (json_request):
            params["firstName"] = json_request.get("firstName", None)
            params["collegeName"] = json_request.get("collegeName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        records = self.get_service().search(params)
        if records and records.get("data"):
            res["success"] = True
            res["result"]["data"] = records["data"]
            res["result"]["lastId"] = Student.objects.last().id
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def get(self, request, params={}):
        student = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (student != None):
            res["success"] = True
            res["result"]["data"] = student.to_json()
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def delete(self, request, params={}):
        student = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (student != None):
            self.get_service().delete(params["id"])
            res["success"] = True
            res["result"]["data"] = student.to_json()
            res["result"]["message"] = "Data has been deleted successfully"
        else:
            res["success"] = False
            res["result"]["message"] = "Data was not deleted"
        return JsonResponse(res)

    def preload(self, request, params={}):
        res = {"result": {}, "success": True}
        college_list = CollegeService().preload()
        preloadList = []
        for x in college_list:
            preloadList.append(x.to_json())
        res["result"]["collegeList"] = preloadList
        return JsonResponse(res)

    def get_service(self):
        return StudentService()
