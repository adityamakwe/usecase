from django.views.decorators.csrf import csrf_exempt
from .ctl.RegistrationCtl import RegistrationCtl
from django.http import JsonResponse
from .ctl.LoginCtl import LoginCtl
from .ctl.UserCtl import UserCtl
from .ctl.RoleCtl import RoleCtl
from .ctl.CollegeCtl import CollegeCtl
from .ctl.CourseCtl import CourseCtl
from .ctl.SubjectCtl import SubjectCtl
from .ctl.FacultyCtl import FacultyCtl
from .ctl.MarksheetCtl import MarksheetCtl
from .ctl.MarksheetMeritListCtl import MarksheetMeritListCtl
from .ctl.StudentCtl import StudentCtl
from .ctl.TimeTableCtl import TimeTableCtl
from .ctl.ChangePasswordCtl import ChangePasswordCtl
from .ctl.ForgetPasswordCtl import ForgetPasswordCtl

@csrf_exempt
def action(request, page, action="get", id=0, pageNo=1):
    methodCall = page + "Ctl()." + action + "(request,{'id':id, 'pageNo':pageNo})"
    response = eval(methodCall)
    return response
