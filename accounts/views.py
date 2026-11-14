from django.shortcuts import render

from rest_framework.views import APIView

from accounts.serializers import UserSerializer

from rest_framework.response import Response

# Create your views here.

class SignUPView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():
            serializer_instance.save()

            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
