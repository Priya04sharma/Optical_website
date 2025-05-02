<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Phonepay payment gateway!")
=======
import json
import hashlib
import base64
import requests
import uuid
import logging
import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

logger = logging.getLogger('payment')

def generate_tran_id():
    """To genarate a unique order number"""
    uuid_part = str(uuid.uuid4()).split('-')[0].upper()  # Get a part of the UUID
    now = datetime.datetime.now().strftime('%Y%m%d')
    return f"TRX{now}{uuid_part}"

def generate_checksum(data, salt_key, salt_index):
    """To Genarate checksum"""
    checksum_str = data + '/pg/v1/pay' + salt_key
    checksum = hashlib.sha256(checksum_str.encode()).hexdigest() + '###' + salt_index
    return checksum

def checkout(request):
    if request.method == 'GET':
        return render(request, 'home.html')

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        """After click pay now it will inisiate payment"""
        amount = request.POST.get('amount') # In rupe
        callback_url = request.build_absolute_uri(reverse('payment:callback'))
        payload = {
            "merchantId":"PGTESTPAYUAT86",
            "merchantTransactionId": generate_tran_id(),
            "merchantUserId": "USR1231",
            "amount": int(amount)*100,  # In paisa
            "redirectUrl": callback_url,
            "redirectMode": "POST",
            "callbackUrl": callback_url,
            "mobileNumber": "9800278886",
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        
        data = base64.b64encode(json.dumps(payload).encode()).decode()
        checksum = generate_checksum(data,)
        final_payload = {
            "request": data,
        }
        
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
        }
        
        try:
            response = requests.post(settings.PHONEPE_INITIATE_PAYMENT_URL+'/pg/v1/pay', headers=headers, json=final_payload)
            data = response.json()
            
            logger.info(data)
            if data['success']:
                url = data['data']['instrumentResponse']['redirectInfo']['url']
                return redirect(url)
            else:
                return redirect('payment:checkout')

        except Exception as e:
            logger.info("initiate payment:: %s", e)
            return redirect('payment:checkout')
        

@csrf_exempt
def payment_callback(request):
    if request.method != 'POST':
        logger.error("Invalid request method: %s", request.method)
        return redirect('payment:checkout')

    try:
        data = request.POST.dict()  # Convert QueryDict to a regular dictionary
        logger.info(data)
        if data.get('checksum') and data.get('code') == "PAYMENT_SUCCESS":
            response = render(request, 'success.html')
            return response
        else:
            logger.info("After payment report:: %s", data)
            return render(request, 'failed.html')
    except Exception as e:
        logger.error("Error parsing request body:: %s", e)
        render(request, 'failed.html')
>>>>>>> 11cf6ae3921d8252c546f1074042babc88cf5416
