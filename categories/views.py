from django.shortcuts import render
# categories/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def category_list_create_view(request):
    # This is placeholder logic. Replace with actual logic.
    if request.method == 'GET':
        categories = [
            {"id": 1, "name": "Technical Support"},
            {"id": 2, "name": "Billing"},
        ]
        return Response(categories, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response({"message": "Category created successfully"}, status=status.HTTP_201_CREATED)
# Create your views here.
