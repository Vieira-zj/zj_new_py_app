from django.db import models

#
# Foreignkey
#


class GenderRef(models.Model):
    text = models.CharField(max_length=10)
    gender = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return self.text


class Student(models.Model):
    Number = models.IntegerField(unique=True, blank=False, null=False)
    # 关联 GenderRef 表的主键，可以使用 to_field 更改
    Gender = models.ForeignKey('GenderRef', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Number}-{self.Gender}'

#
# Test
#


def init_data():
    male = GenderRef(text='male', gender=1)
    male.save()
    female = GenderRef(text='female', gender=2)
    female.save()

    s1 = Student(id=None, Number=1234, Gender=male)
    s1.save()
    s2 = Student(id=None, Number=2345, Gender=female)
    s2.save()


def init_student_data():
    male = GenderRef.objects.filter(gender=1).get()
    female = GenderRef.objects.filter(gender=2).get()

    base_num = 3456
    for i in range(5):
        gender = male if i % 2 == 0 else female
        s = Student(id=None, Number=base_num+i, Gender=gender)
        s.save()


def select_data():
    print('gender:')
    rows = GenderRef.objects.all()
    for row in rows:
        print(row)

    print('student:')
    rows = Student.objects.all()
    for row in rows:
        print(row)


def get_all_female_student():
    female = GenderRef.objects.get(text='female')
    print('female students:')
    # 反向查询：子表表名+_set
    female_students = female.student_set.all()
    for student in female_students:
        print(student)
