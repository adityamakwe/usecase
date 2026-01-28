import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl
from ..service.UserService import UserService
from ..utility.DataValidator import DataValidator
from ..utility.JwtUtility import generate_jwt_token


class LoginCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['loginId'] = requestForm.get('loginId', '')
        self.form['password'] = requestForm.get('password', '')

    def input_validation(self):
        super().input_validation()

        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form["loginId"])):
            inputError["loginId"] = "Login ID is required"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form['loginId'])):
                inputError['loginId'] = "Login Id must be email"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password is required"
            self.form["error"] = True

        return self.form["error"]

    def auth(self, request, params={}):
        # json_request = json.loads(request.body)
        # ✅ Handle CORS preflight
        if request.method == "OPTIONS":
            return JsonResponse({}, status=200)

        # ✅ Safe JSON parsing
        try:
            json_request = json.loads(request.body.decode("utf-8")) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "result": {"message": "Invalid JSON"}},
                status=400
            )
        self.request_to_form(json_request)
        res = {"result":{},"success":True}
        if (self.input_validation()):
            res["success"] = False
            res["result"]["inputerror"] = self.form["inputError"]
        else:
            user = self.get_service().authenticate(self.form)
            if (user is None):
                res['success'] = False
                res["result"]["message"] = "Login ID & Password is Invalid"
            else:
                # res["result"]["data"] = user.to_json()
                token = generate_jwt_token(user.loginId)
                res["result"]["data"] = user.to_json()
                res["result"]["token"] = token

        return JsonResponse(res)

    def get_service(self):
        return UserService()