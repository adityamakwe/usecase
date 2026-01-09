from django.http import HttpResponse
from abc import ABC, abstractmethod


class BaseCtl(ABC):
    dynamic_preload = {}
    static_preload = {}
    page_list = {}

    def __init__(self):
        self.form = {}
        self.form["id"] = 0
        self.form["message"] = ""
        self.form["error"] = False
        self.form["inputError"] = {}
        self.form["pageNo"] = 1
        self.form["preload"] = {}

    def preload(self, request, params={}):
        pass

    def request_to_form(self, requestForm):
        pass

    def form_to_model(self, obj):
        pass

    def model_to_form(self, obj):
        pass

    def input_validation(self):
        self.form["error"] = False
        self.form["message"] = ""


    @abstractmethod
    def get_service(self):
        pass
