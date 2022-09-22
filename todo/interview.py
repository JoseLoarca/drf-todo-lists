from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Todo

class Interview(APIView):

    def get(self, request):
        
        return Response(
            {"result": "data result"}, 
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        print(type(request.data))
        
        return Response(
            {"result": "post result"}, 
            status=status.HTTP_200_OK
        )
    
