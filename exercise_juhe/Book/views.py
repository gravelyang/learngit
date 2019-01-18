from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Avg,Count,Max, Min,F
from .models import *
from django.db import connection

def index(request):
    result = Book.objects.aggregate(Avg('price'))
    print(result)
    print(connection.queries)
    return HttpResponse('success')

def index2(request):
    # result = Book.objects.aggregate(avg=Avg('bookorder__price'))
    # print(result)
    results = Book.objects.annotate(avg=Avg('bookorder__price'))
    # print(results)
    for result in results:
        print('%s：%s' % (result.name, result.avg))
    return HttpResponse('success')

def index3(request):
    # results = Author.objects.aggregate(email_nums=Count('email', distinct=True))
    # print(results)
    results = Book.objects.annotate(book_nums=Count('bookorder__id'))
    for result in results:
        print('%s：%s' % (result.name, result.book_nums))
    return HttpResponse('success')

def index4(request):
    results = Author.objects.aggregate(max=Max('age'), min=Min('age'))
    print(results)
    prices = Book.objects.annotate(max=Max('bookorder__price'), min=Min('bookorder__price'))
    print(prices)
    for price in prices:
        print('%s：最大：%s, 最小：%s' % (price.name, price.max, price.min))

    return HttpResponse('index4')

def index5(request):
    books = Book.objects.values_list('author__name', flat=True)
    for book in books:
        print(book)
    return HttpResponse('index5')

def index6(request):
    books = Book.objects.select_related('author', )
    for book in books:
        print(book.author.name)
    print(connection.queries)
    return HttpResponse('index6')



def index7(request):
    books = Book.objects.prefetch_related('bookorder_set')
    for book in books:
        print(book.author)
        orders = book.bookorder_set.all()
        for order in orders:
            print(order.price)
    print(connection.queries)
    return HttpResponse('index7')


def index8(request):
    books = Book.objects.defer('name')
    for book in books:
        print(book.id)
    print(connection.queries)
    return HttpResponse('index8')

def index9(request):
    publisher = Publisher.objects.get_or_create(name='人民邮电出版社')
    print(publisher)
    print(connection.queries)
    return HttpResponse('index9')

def index10(request):
    # publisher = Publisher.objects.bulk_create([
    #     Publisher(name='abc出版社'),
    #     Publisher(name='12出版社')
    # ])
    publish_list = ['戏剧社', '拍摄社', '机密的出版社', ]
    publishers = Publisher.objects.values_list('name', flat=True)
    print(publishers)
    farm = []
    for publish in publish_list:
        if not publish in publishers:
            farm.append(Publisher(name=publish))
    Publisher.objects.bulk_create(farm)
    print(connection.queries)
    return HttpResponse('index10')

def index11(request):
    result = Book.objects.filter(name__icontains='演义').exists()
    print(result)
    return HttpResponse('index11')

def index12(request):
    books = Book.objects.filter(bookorder__price__gte=120).distinct()
    for book in books:

        print(book)
    print(connection.queries)
    return HttpResponse('index12')