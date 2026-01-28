from ..models import User
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService


class ForgetPasswordService(BaseService):

    def find_by_login(self, params):
        user = self.get_model().objects.get(loginId=params['loginId'])
        return user

    def get_model(self):
        return User
