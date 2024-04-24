# import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from datetime import datetime
import requests
# import local data
from .serializers import clientSerializer,ServiceSerializer
from .models import Client,Service
from .savepdf import generate_pdf

BASE_URL = "http://mb-stage:5002/API/"

@csrf_exempt
@api_view(['GET'])
def check_client_existing(request):
    if request.method == 'GET':
        national_id = request.query_params.get('national_id', None)
        account_id = request.query_params.get('account_id', None)
        client_name = request.query_params.get('client_name', None)
        
        if not national_id:
            return Response({"error": "Provide national_id in the form data"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Client.objects.get(national_id=national_id)
            
            if (account_id and item.account_id != account_id):
                return Response({"status": False}, status=status.HTTP_200_OK)

            return Response({"status": True}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"status": False}, status=status.HTTP_200_OK)        

@csrf_exempt
@api_view(['GET'])
def withdrawal_availability(request):
    if request.method == 'GET':
        national_id = request.query_params.get('national_id', None)
        account_id = request.query_params.get('account_id', None)
        amount = request.query_params.get('amount', None)
        
        if not national_id:
            return Response({"error": "Provide national_id in the form data"}, status=status.HTTP_400_BAD_REQUEST)

        if not account_id:
            return Response({"error": "Provide account_id in the form data"}, status=status.HTTP_400_BAD_REQUEST)

        if not amount :
            return Response({"error": "Provide amount in the form data"}, status=status.HTTP_400_BAD_REQUEST)

        if int(amount.replace(',','')) < 0:
            return Response({"error": "Provide positive amount in the form data"}, status=status.HTTP_400_BAD_REQUEST)
    
        if int(amount.replace(',','')) > 5000:
            return Response({"status": False}, status=status.HTTP_200_OK)
        return Response({"status": True}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def count_videos_terms_and_conditions(request):
    if request.method == 'GET':
        return Response({"count": 5}, status=status.HTTP_200_OK)

## open account
class ClientViews(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = clientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ## TO DO print on paper
            info = serializer.data
            service_num = 0
            created_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            generate_pdf(pdf_name=f"{info['national_id']}_open_account_{created_time}",
                         service_num = service_num,
                         info=info)
            
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
## Withdrawal or deposit     
class ServiceViews(APIView):
    @csrf_exempt
    def post(self, request):
        data=request.data
        data["amount"]= int(data["amount"].replace(',',''))
        serializer = ServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            ## TO DO print file on paper
            info = serializer.data
            item = Client.objects.get(national_id=info["client"])
            info["account_id"] = item.account_id if item.account_id is not None else "غير متوفر"
            info["client_name"] = item.client_name
            service_num = 2 if 'سحب' in info['service_name']  else 1
            created_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            generate_pdf(pdf_name=f"{info['client']}_{'deposit' if service_num == 1 else 'withdrawal'}_{created_time}",
                         service_num = service_num,
                         info=info)
            
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)