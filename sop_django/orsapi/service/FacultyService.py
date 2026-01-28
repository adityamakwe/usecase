from ..models import Faculty
from .BaseService import BaseService
from ..utility.DataValidator import DataValidator
from django.db import connection


class FacultyService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo']) * self.pageSize
        sql = "select * from sos_faculty where 1=1"
        val = params.get("firstName", None)
        val2 = params.get("email", None)
        if (DataValidator.isNotNull(val)):
            sql += " and firstName like '" + val + "%%'"
        if (DataValidator.isNotNull(val2)):
            sql += " and email like '" + val2 + "%%'"
        sql += " limit %s, %s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = (
            'id', 'firstName', 'lastName', 'email', 'password', 'address', 'gender', 'dob', 'collegeId', 'collegeName'
            , 'subjectId', 'subjectName', 'courseId', 'courseName')
        res = {
            "data": [],
        }
        params["index"] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Faculty
