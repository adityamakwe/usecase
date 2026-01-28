import json

from django.http import JsonResponse

from .BaseCtl import BaseCtl
from django.shortcuts import render
from ..service.MarksheetMeritListService import MarksheetMeritListService


class MarksheetMeritListCtl(BaseCtl):

    def display(self, request, params={}):
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'form': self.form, 'pageList': self.page_list})
        return res

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {"result": {}, "success": True}
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        return JsonResponse(res)

    def get_service(self):
        return MarksheetMeritListService()
