from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Avg, Sum, Count, Q, Max, Min, F

def index1(request):
    '''查询平均成绩大于60分的学生的id和平均成绩'''
    students = Student.objects.annotate(avg = Avg('score__number')).filter(score__number__gt=60).values('avg', 'id')
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
    students = Student.objects.exclude(score__course__teacher__name='李老师').values('id', 'name')
    print(type(students))
    for student in students:
        print(student)
    return HttpResponse('index4')

def index5(request):
    '''查询学过黄老师所教所有课的学生的id，姓名'''
    # students = Student.objects.filter(score__course__teacher__name='黄老师').values('id', 'name')
    students = Student.objects.annotate(count1=Count('score__course',filter=Q(score__course__teacher__name='黄老师'))).filter(count1=Course.objects.filter(teacher__name='黄老师').count()).values('id', 'name')

    for student in students:
        print(student)
    return HttpResponse('index5')

def index6(request):
    '''查询所有课程成绩小于60分的同学的id,姓名'''
    students = Student.objects.filter(score__number__lt=60).values('id','name')
    for student in students:
        print(student)
    return HttpResponse('index6')

def index7(request):
    '''查询没有学完所有课的同学的id,姓名'''
    students = Student.objects.annotate(count=Count('score__id'))
    for student in students:
        if student.count < 3:
            print(student.id, student.name)
    return HttpResponse('index7')

def index8(request):
    '''查询学过课程为1和2的所有同学的id,姓名'''
    students = Student.objects.filter(score__course__in=[1,2]).values('id','name').distinct()
    for student in students:
        print(student)
    return HttpResponse('index8')

def index9(request):
    '''查询所有学生的姓名、平均分、并且按照平均分从高到低排序'''
    students = Student.objects.annotate(avg=Avg('score__number')).order_by('-avg').values('name','avg')
    for student in students:
        print(student)
    return HttpResponse('index9')

def index10(request):
    '''查询各科成绩的最高和最低分，以以下形式显示：课程ID,课程名称，最高分，最低分'''
    courses = Course.objects.annotate(max=Max('score__number'), min=Min('score__number')).values('id','name','max','min')
    for course in courses:
        print(course)
    return HttpResponse('index10')

def index11(request):
    '''查询每门课程的平均成绩，按照平均成绩进行排序'''
    courses = Course.objects.annotate(avg=Avg('score__number')).order_by('avg').values('name','avg')
    for course in courses:
        print(course)
    return HttpResponse('index11')

def index12(request):
    '''统计共有多少女生、多少男生'''
    student_1 = Student.objects.filter(gender=1).count()
    student_2 = Student.objects.filter(gender=2).count()
    print('共有男生:%s人,女生:%s人' % (student_1,student_2))
    return HttpResponse('index12')

def index13(request):
    '''将“黄老师的每一门课程都在原来的基础上加五分”'''
    courses = Course.objects.filter(teacher__name='黄老师').annotate(score__number=F('score__number')+5).values('name','score__number').distinct()
    for course in courses:
        print(course)
    return HttpResponse('index14')

def index14(request):
    '''查询两门以上不及格的同学的id、姓名、以及不及格课程数'''
    students = Student.objects.filter(score__number__lt=60).annotate(count=Count('score__course')).filter(count__gte=2).values('id','name','count')
    for student in students:
        print(student)
    return HttpResponse('index15')

def index15(request):
    '''查询每门课程的选课人数'''
    courses = Course.objects.annotate(count=Count('score__id')).values('name', 'count')
    for course in courses:
        print(course)
    return HttpResponse('index16')