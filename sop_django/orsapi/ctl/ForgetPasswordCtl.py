import json
from django.http import JsonResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ..utility.DataValidator import DataValidator
from ..service.ForgetPasswordService import ForgetPasswordService
from ..service.EmailService import EmailService
from ..service.EmailMessege import EmailMessege
from ..models import User


class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form['loginId'] = requestFrom.get('loginId','')

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if DataValidator.isNull(self.form['loginId']):
            inputError['loginId'] = "Login Id can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['loginId'])):
                inputError['loginId'] = "Login ID must be like student@gmail.com"
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
            try:
                user = self.get_service().find_by_login(self.form)
                emailMessage = EmailMessege()
                emailMessage.to = [user.loginId]
                emailMessage.subject = "Forget Password"

                mail_response = EmailService.send(emailMessage, "forgetPassword", user)

                if mail_response == 1:
                    res["success"] = True
                    res["result"]["message"] = "Your password has been sent successfully"
                else:
                    res["success"] = False
                    res["result"]["message"] = "Please check your Internet connection"
            except User.DoesNotExist:
                res["success"] = True
                res["result"]["message"] = "Login ID is incorrect"
            except Exception as e:
                res["success"] = False
                res["result"]["message"] = f"An unexpected error occurred: {str(e)}"
        return JsonResponse(res)

    def get_service(self):
        return ForgetPasswordService()
