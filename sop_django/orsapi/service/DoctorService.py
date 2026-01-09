from ..models import Doctor
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class DoctorService(BaseService):

    def authenticate(self, params):
        loginId = params.get("loginId", None)
        password = params.get("password", None)

        q = self.get_model().objects.filter()

        if (DataValidator.isNotNull(loginId)):
            q = q.filter(loginId=loginId)

        if (DataValidator.isNotNull(password)):
            q = q.filter(password=password)

        if (q.count() == 1):
            return q[0]
        else:
            return None

    def search(self, params):
        pageNo = ((params["pageNo"]) * self.pageSize)
        sql = "select * from sos_doctor where 1=1"
        val = params.get("firstName", None)
        val2 = params.get("expertise", None)
        print('=================',val)
        if DataValidator.isNotNull(val):
            sql += " and firstName like '" + val + "%%'"

        if DataValidator.isNotNull(val2):
            sql += " and expertise = '" + val2 + "'"

        sql += " limit %s, %s"
        print(sql)
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "firstName", "lastName",
                      "dob", "mobileNumber", "expertise")
        res = {
            "data": [],
        }
        params["index"] = ((params['pageNo'] - 1) * self.pageSize)
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['maxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    # def search(self, params):
    #     page = int(params.get("pageNo", 1))
    #     if page < 1:
    #         page = 1
    #     pageNo = ((params["pageNo"] - 1) * self.pageSize)
    #
    #     sql = "SELECT * FROM sos_doctor WHERE 1=1"
    #     values = []
    #
    #     search = params.get("search", None)
    #
    #     if DataValidator.isNotNull(search):
    #         sql += " AND (firstName LIKE %s OR expertise LIKE %s)"
    #         values.append(search + "%")  # firstName starts with
    #         values.append("%" + search + "%")  # expertise contains
    #
    #     sql += " LIMIT %s, %s"
    #     values.append(pageNo)
    #     values.append(self.pageSize)
    #
    #     print(sql, values)
    #
    #     cursor = connection.cursor()
    #     cursor.execute(sql, values)
    #     result = cursor.fetchall()
    #
    #     columnName = ("id", "firstName", "lastName", "dob", "mobileNumber", "expertise")
    #
    #     res = {"data": []}
    #     params["index"] = pageNo
    #
    #     for x in result:
    #         res["data"].append({columnName[i]: x[i] for i in range(len(x))})
    #
    #     return res

    def get_model(self):
        return Doctor
