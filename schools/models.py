from django.db import models


# Create your models here.
class BasicInfo(models.Model):
    establish_date = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    rooms = models.IntegerField(blank =True, null = True)
    teaching_staffs = models.IntegerField(blank =True, null = True)
    non_teaching_staffs = models.IntegerField(blank =True, null = True)

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField()
    district = models.CharField(max_length=30)
    edu_district = models.CharField(max_length=30)
    sub_district = models.CharField(max_length=30)
    url_id = models.IntegerField(blank =True, null = True)
    basic_info = models.ForeignKey(BasicInfo,on_delete=models.CASCADE,null=True)
    created_on = models.DateTimeField(auto_now_add = True)
    
    # staff_strength = models.ForeignKey(StaffStrength,on_delete=models.CASCADE,null=True)
    #staff = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class StaffStrength(models.Model):
    school = models.ForeignKey(School,on_delete=models.CASCADE,related_name='staffstrength')
    year = models.CharField(max_length =30)
    designation = models.CharField(max_length=50)
    strength = models.IntegerField(blank =True, null = True)

class StudentStrength(models.Model):
    school = models.ForeignKey(School,on_delete=models.CASCADE,related_name='students')
    course = models.IntegerField()
    strength = models.IntegerField(blank =True, null = True)
    sampoorna = models.IntegerField(blank =True, null = True)
    available_uid = models.IntegerField(blank =True, null = True)
    valid_uid = models.IntegerField(blank =True, null = True)
    partialy_match_uid = models.IntegerField(blank =True, null = True)
    invalid_uid = models.IntegerField(blank =True, null = True)
    none = models.IntegerField(blank =True,null = True)
    


class Staff(models.Model):
    school = models.ForeignKey(School,on_delete=models.CASCADE,related_name='staffs')
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    date_of_join = models.DateField()

    def __str__(self):
        return self.name

"""
class SubDistrict(models.Model):
    name = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
"""