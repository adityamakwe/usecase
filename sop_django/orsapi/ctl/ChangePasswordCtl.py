import json
from django.http import JsonResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..utility.DataValidator import DataValidator
from ..models import User
from ..service.ChangePasswordService import ChangePasswordService
from ..service.EmailService import EmailService
from ..service.EmailMessege import EmailMessege
from ..service.UserService import UserService


class ChangePasswordCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['oldPassword'] = requestForm.get("oldPassword",'')
        self.form['newPassword'] = requestForm.get("newPassword",'')
        self.form['confirmPassword'] = requestForm.get("confirmPassword",'')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.oldPassword = self.form['oldPassword']
        obj.newPassword = self.form['newPassword']
        obj.confirmPassword = self.form['confirmPassword']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['oldPassword'] = obj.oldPassword
        self.form['newPassword'] = obj.newPassword
        self.form['confirmPassword'] = obj.confirmPassword

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['oldPassword'])):
            inputError['oldPassword'] = "Old Password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['newPassword'])):
            inputError['newPassword'] = "New Password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['confirmPassword'])):
            inputError['confirmPassword'] = "Confirm Password can not be null"
            self.form['error'] = True

        return self.form['error']

    def submit(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {"result": {}, "success": True}
        if (self.input_validation()):
            res["success"] = False
            res["result"]["inputerror"] = self.form["inputError"]
        else:
            q = User.objects.filter(id=self.form['id'], password=self.form['oldPassword'])
            if q.count() > 0:
                if self.form['newPassword'] == self.form['confirmPassword']:
                    if True:
                        user = q[0]
                        user.password = self.form['newPassword']
                        user.confirmPassword = self.form['confirmPassword']
                        UserService().save(user)
                        emailMessage = EmailMessege()
                        emailMessage.to = [user.loginId]
                        emailMessage.subject = "Change Password"

                        mail_response = EmailService.send(emailMessage, "changePassword", user)
                        if mail_response == 1:

                            res["success"] = True
                            res["result"]["message"] = "your password has been changed successfully, please check your mail..."
                        else:
                            res["success"] = False
                            res["result"]["message"] = "Please Check Your Internet Connection"
                else:
                    res["success"] = False
                    res["result"]["message"] = "Confirm Password are not matched"
            else:
                res["success"] = False
                res["result"]["message"] = "Old Password is wrong"
        return JsonResponse(res)

    def get_service(self):
        return ChangePasswordService()
