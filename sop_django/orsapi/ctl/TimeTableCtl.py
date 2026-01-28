import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from ..models import TimeTable
from ..service.CourseService import CourseService
from ..service.SubjectService import SubjectService
from ..service.TimeTableService import TimeTableService


class TimeTableCtl(BaseCtl):

    # def preload(self, request, params={}):
    #     self.course_List = CourseService().preload()
    #     self.subject_List = SubjectService().preload()

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['examTime'] = requestForm.get('examTime','')
        self.form['examDate'] = requestForm.get('examDate','')
        self.form['courseId'] = requestForm.get('courseId','')
        self.form['subjectId'] = requestForm.get('subjectId','')
        self.form['semester'] = requestForm.get('semester','')

        if self.form['courseId'] != '':
            course = CourseService().get(self.form['courseId'])
            self.form["courseName"] = course.name

        if self.form['subjectId'] != '':
            subject = SubjectService().get(self.form['subjectId'])
            self.form["subjectName"] = subject.name

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['examTime'] = obj.examTime
        self.form['examDate'] = obj.examDate.strftime("%Y-%m-%d")
        self.form['courseId'] = obj.courseId
        self.form['courseName'] = obj.courseName
        self.form['subjectId'] = obj.subjectId
        self.form['subjectName'] = obj.subjectName
        self.form['semester'] = obj.semester

    def form_to_model(self, obj):
        course = CourseService().get(self.form['courseId'])
        subject = SubjectService().get(self.form['subjectId'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.examTime = self.form['examTime']
        obj.examDate = self.form['examDate']
        obj.courseId = self.form['courseId']
        obj.courseName = course.name
        obj.subjectId = self.form['subjectId']
        obj.subjectName = subject.name
        obj.semester = self.form['semester']
        return obj

    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['examTime'])):
            inputError['examTime'] = "Exam Time can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['examDate'])):
            inputError['examDate'] = "Exam Date can not be null"
            self.form['error'] = True

        if (DataValidator.isNotNull(self.form['examDate'])):
            if (DataValidator.isDate(self.form['examDate'])):
                inputError['examDate'] = "Incorrect date format, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['courseId'])):
            inputError['courseId'] = "Course can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['subjectId'])):
            inputError['subjectId'] = "Subject can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['semester'])):
            inputError['semester'] = "Semester can not be null"
            self.form['error'] = True
        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {
            'form': self.form,
            'courseList': self.course_List,
            'subjectList': self.subject_List
        })
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
                duplicate = TimeTable.objects.exclude(id=pk).filter(
                    subjectId=self.form['subjectId'],
                    examTime=self.form['examTime'],
                    examDate=self.form['examDate']
                )
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Exam Time, Exam Date, Subject name already exists"
                    return JsonResponse(res)
                else:
                    timeTable = self.form_to_model(TimeTable())
                    self.get_service().save(timeTable)
                    self.form['id'] = timeTable.id
                    res["success"] = True
                    res["result"]["message"] = "Timetable updated successfully"
                    return JsonResponse(res)
            else:
                duplicate = TimeTable.objects.filter(
                    subjectId=self.form['subjectId'],
                    examTime=self.form['examTime'],
                    examDate=self.form['examDate']
                )
                if duplicate.count() > 0:
                    res["success"] = False
                    res["result"]["message"] = "Exam Time, Exam Date, Subject name already exists"
                    return JsonResponse(res)

                else:
                    timeTable = self.form_to_model(TimeTable())
                    self.get_service().save(timeTable)
                    res["success"] = True
                    res["result"]["message"] = "Timetable added successfully"
                    return JsonResponse(res)
        return JsonResponse(res)

    def search(self, request, params={}):
        json_request = json.loads(request.body)
        res = {"result": {}, "success": True}
        if (json_request):
            params["courseName"] = json_request.get("courseName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        records = self.get_service().search(params)
        if records and records.get("data"):
            res["success"] = True
            res["result"]["data"] = records["data"]
            res["result"]["lastId"] = TimeTable.objects.last().id
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def get(self, request, params={}):
        timetable = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (timetable != None):
            res["success"] = True
            res["result"]["data"] = timetable.to_json()
        else:
            res["success"] = False
            res["result"]["message"] = "No record found"
        return JsonResponse(res)

    def delete(self, request, params={}):
        timetable = self.get_service().get(params["id"])
        res = {"result": {}, "success": True}
        if (timetable != None):
            self.get_service().delete(params["id"])
            res["success"] = True
            res["result"]["data"] = timetable.to_json()
            res["result"]["message"] = "Data has been deleted successfully"
        else:
            res["success"] = False
            res["result"]["message"] = "Data was not deleted"
        return JsonResponse(res)

    def preload(self, request, params={}):
        res = {"result": {}, "success": True}
        course_list = CourseService().preload()
        subject_list = SubjectService().preload()
        preloadList = []
        preloadList1 = []
        for x in course_list:
            preloadList.append(x.to_json())
        res["result"]["courseList"] = preloadList

        for x in subject_list:
            preloadList1.append(x.to_json())
        res["result"]["subjectList"] = preloadList1

        return JsonResponse(res)

    def get_service(self):
        return TimeTableService()
