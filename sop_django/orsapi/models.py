from django.db import models


# Create your models here.

class Doctor(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(max_length=50)
    mobileNumber = models.CharField(max_length=50, default='')
    roleName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'dob': self.dob.strftime('%Y-%m-%d'),
            'expertise': self.expertise
        }
        return data

    class Meta:
        db_table = 'sos_doctor'

class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def to_json(self):
        data ={
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return data

    class Meta:
        db_table = 'sos_role'