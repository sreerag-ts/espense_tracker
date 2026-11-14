from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework import authentication,permissions

from transactions.models import Expense

from transactions.serializer import ExpenseSerializer

from rest_framework.response import Response

class ExpenseListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        qs = Expense.objects.filter(owner=auth_user)

        serializer_instance = ExpenseSerializer(qs,many=True)

        return Response(serializer_instance.data)

    