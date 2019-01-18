from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Avg, Sum, Count

def index1(request):
    '''查询平均成绩大于60分的学生的id和平均成绩'''
    students = Student.objects.annotate(avg = Avg('score__number')).filter(score__number__gt=60)
    for student in students:
        print('='*20)
        print('同学id为：%s,平均成绩为：%s' % (student.id, student.avg))
    return HttpResponse('index1')


def index2(request):
    '''查询所有同学的id,姓名、选课的数、总成绩'''
    students = Student.objects.annotate(sum=Sum('score__number'), count=Count('score'))
    for student in students:
        print('='*20)
        print('同学的id为：%s,姓名：%s, 选课数:%s,总成绩：%s' % (student.id, student.name, student.count, student.sum))
    return HttpResponse('index2')

def index3(request):
    '''查询姓李的老师的个数'''
    teacher_nums = Teacher.objects.filter(name__startswith='李').count()
    print('姓李的老师的个数为：%s' % teacher_nums)
    return HttpResponse('index3')


def index4(request):
    '''查询没学过李老师课程的学生的id,姓名'''
    course3 = Course.objects.get(teacher_id=3)
    student_nums = Score.objects.filter(course_id=3)
    for student in students:
        print(student.count)
    return HttpResponse('index4')