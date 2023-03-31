```python
INSTALLED_APPS = [
    
    'app',
    'rest_framework',
]
```
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title
```
## app/serializers.py
```python
from .models import Book
from rest_framework import serializers


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'
```


```python
from django.contrib import admin
from .models import Book


admin.site.register(Book)

```

```python
from django.contrib import admin
from django.urls import path
from app.views import books,book_detail,book_create,book_delete,book_update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',books,name='books_list'),
    path('create/', book_create, name='book_create'),
    path('detail/<int:pk>',book_detail, name='book_detail'),
    path('update/<int:pk>',book_update, name='book_update'),
    path('delete/<int:pk>',book_delete, name='book_delete'),

]

```


```python
from django.shortcuts import render
from .serializers import BookSerializers
from rest_framework.decorators import api_view
from app.models import Book
from rest_framework.response import Response


"""
--> Query
--> data=serilize(Query).data
--> Response(data)
"""

@api_view(['GET'])
def books(request):
    queries=Book.objects.all()
    serializer=BookSerializers(queries,many=True)
    books=serializer.data
    return Response({'books':books})



@api_view(['GET'])
def book_detail(request,pk):
    try:
        #query=Book.objects.get(pk=pk)
        query= Book.objects.filter(pk=pk).values()[0]
        serializer=BookSerializers(query)
        book=serializer.data
        return Response({'book':book})
        
    except:
        Response('Invalid Id')

@api_view(['POST'])
def book_create(request):
    PostData=request.data
    serializer=BookSerializers(data=PostData)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':serializer.data})
    return Response('Invalid Data')
@api_view(['PUT'])
def book_update(request,pk):
    try:
        PostData=request.data
        query=Book.objects.get(pk=pk)
    except:
        return Response('Book doesnt exist with given Id')
    serializer=BookSerializers(query,data=PostData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response('Something  Wrong with Serializer')



@api_view(['DELETE'])
def book_delete(request,pk):
    try:
        query=Book.objects.get(pk=pk)
        query.delete()
        return Response('Succeffuly Deleted')
    except:
        return Response({'message':'Wrong Id or query doesnt exist'})
    

    
```