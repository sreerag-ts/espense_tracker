from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView

from rest_framework import authentication,permissions

from transactions.models import Expense

from transactions.serializer import ExpenseSerializer

from rest_framework.response import Response

class ExpenseListCreateView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]


    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        qs = Expense.objects.filter(owner=auth_user)

        serializer_instance = ExpenseSerializer(qs,many=True)

        return Response(serializer_instance.data)

    def post(self,request):
    
            form_data = request.data
    
            auth_user = request.user
    
            serializer_instance = ExpenseSerializer(data=form_data)
    
            if serializer_instance.is_valid():
    
                serializer_instance.save(owner=auth_user)
    
                return Response(serializer_instance.data)
    
            else:
    
                return Response(serializer_instance.errors)


from transactions.permissions import IsOwner

class ExpenseRetrieveUpdateDeleteView(APIView):

    #authentication_classes=[authentication.BasicAuthentication]

    authentication_classes = [authentication.TokenAuthentication]

    #permission_classes = [permissions.IsAuthenticated]

    permission_classes = [IsOwner]

    def get(self,request,pk=None):

        #qs = Expense.objects.get(id=pk)

        qs = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,qs)


        serializer_instance = ExpenseSerializer(qs)

        return Response(serializer_instance.data)

    def put(self,request,pk=None):

         instance = Expense.objects.get(id=pk)

         self.check_object_permissions(request,instance)

         form_data = request.data

         serializer_instance = ExpenseSerializer(data=form_data,instance=instance)

         if serializer_instance.is_valid():

              serializer_instance.save()

              return Response(serializer_instance.data)

         else:

              Response(serializer_instance.errors)


    def delete(self,request,pk=None):

         instance = get_object_or_404(Expense,id=pk)
         
         self.check_object_permissions(request,instance)

         instance.delete()

         return Response({"message":"deleted"})



from datetime import datetime
from django.db.models import Sum

class ExpenceSummaryView(APIView):
      #authentication_classes = [authentication.BasicAuthentication]
      authentication_classes = [authentication.TokenAuthentication]

      permission_classes = [permissions.IsAuthenticated]

      def get(self,request):

           auth_user_expences = Expense.objects.filter(owner=request.user)

           response_data ={
                "todays_total":0,
                "monthly_total":0
           }
           
           #date

           curr_date = datetime.today().date()

           todays_total = auth_user_expences.filter(created_at__date = curr_date).values("amount").aggregate(total=Sum("amount")).get("total")

           #month

           curr_month = datetime.today().month

           curr_year = datetime.today().year

           monthly_total = auth_user_expences.filter(created_at__month=curr_month,created_at__year=curr_year).values("amount").aggregate(total=Sum("amount")).get("total")

           response_data["todays_total"]= todays_total
           response_data["monthly_total"]=monthly_total


           return Response(response_data)
      

   
    