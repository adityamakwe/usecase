from ..models import User
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService


class ChangePasswordService(BaseService):

    def get_model(self):
        return User
