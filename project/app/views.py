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
    

    



