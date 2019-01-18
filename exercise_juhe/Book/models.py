from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'publisher'

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'author'

class Book(models.Model):
    name = models.CharField(max_length=300)
    price = models.FloatField()
    pages = models.IntegerField()
    rating = models.FloatField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publish = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book'

class BookOrder(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.FloatField()