from django.shortcuts import render
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import PaymentTransaction
from users.models import UserToken

from django.shortcuts import render, redirect
from users.models import UserToken
from django.conf import settings
from datetime import datetime, timedelta
import uuid
import hmac
import hashlib



def home(request):
     return render(request, "base/index.html")

def checkout_membership(request):
    context= {}
    if request.method == "POST":
        product_name = "OSP Shop"
        product_price = 333
        membership_start = datetime.now()
        
        pp_Amount = 333
        current_datetime = datetime.now()
        pp_TxnDateTime = current_datetime.strftime('%Y%m%d%H%M%S')
        expiry_datetime = current_datetime + timedelta(hours=1)
        pp_TxnExpiryDateTime = expiry_datetime.strftime('%Y%m%d%H%M%S')
        tr_description = f"Payment for registration of {product_name}"
        
        token = uuid.uuid4()        
        UserToken.objects.create(user=request.user, token=token)
        
        pp_TxnRefNo = "T" + (pp_TxnDateTime)
        post_data = {
            "pp_Version": "1.0",
            "pp_TxnType": "",
            "pp_Language": "EN",
            "pp_MerchantID": settings.JAZZCASH_MERCHANT_ID,
            "pp_SubMerchantID": "",
            "pp_Password": settings.JAZZCASH_PASSWORD,
            "pp_BankID": "TBANK",
            "pp_ProductID": "RETL",
            "pp_TxnRefNo": str(pp_TxnRefNo),
            "pp_Amount": str(pp_Amount),
            "pp_TxnCurrency": "PKR",
            "pp_TxnDateTime": str(pp_TxnDateTime),
            "pp_TxnExpiryDateTime": pp_TxnExpiryDateTime,
            "pp_BillReference": "billRef",
            "pp_Description": tr_description,
            "pp_ReturnURL": settings.JAZZCASH_RETURN_URL,
            "pp_SecureHash": "",
            "ppmpf_1": token,
            "ppmpf_2": "membership",
            "ppmpf_3": "3",
            "ppmpf_4": "4",
            "ppmpf_5": "5",
        }
            
        sorted_string = "&".join(f"{key}={value}" for key , value in sorted(post_data.items()) if value != "")
        pp_SecureHash = hmac.new(
            settings.JAZZCASH_INTEGRITY_SALT.encode(),
            sorted_string.encode(),
            hashlib.sha256
        ).hexdigest()
        post_data['pp_SecureHash'] = pp_SecureHash
        context = {
            'product_name':product_name,
            'product_price':product_price,
            'membership_start':membership_start,
            'post_data':post_data,
        }
        redirect("base/index.html")

    return render(request, "base/join_membership.html", context)


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        # Token-based authentication
        token = request.POST.get('ppmpf_1')  # Retrieve the token from the request
        payment_for = request.POST.get('ppmpf_2')
        
        if token:
            try:
                user_token = UserToken.objects.get(token=token)
                user = user_token.user
                login(request, user, backend='users.backends.EmailBackend')
                user_token.delete()  # Optionally delete the token after use
            except UserToken.DoesNotExist:
                return render(request, 'base/payment_failed.html', {"message": "User token is invalid or expired"})
        else:
            return render(request, 'base/payment_failed.html', {"message": "No token provided."})

        # Proceed with payment processing
        transaction_id = request.POST.get('pp_TxnRefNo')
        amount = request.POST.get('pp_Amount')
        status = request.POST.get('pp_ResponseCode')
        message = request.POST.get('pp_ResponseMessage')

        # Save transaction details to the database
        PaymentTransaction.objects.create(
            transaction_id=transaction_id,
            amount=amount,
            status=status
        )

        # Assuming '199' is the success code for the payment
        if status == '199':
            if request.user.is_authenticated:
                if payment_for == "ss":
                    try:
                       message = "Payment successfully"
                       return render(request, 'base/payment_success.html', {"message": message})           
                    except Exception as e:
                        message = "Some error occurred while trying"
                        return render(request, 'base/payment_failed.html', {"message": message})
                
            else:
                message = "Some error occurred while authentication the user"
                return render(request, 'base/payment_failed.html', {"message": message})
        else:
            return render(request, 'base/payment_failed.html', {"message": message, "status": status})
    
    return render(request, 'base/payment_failed.html', {'error': 'Invalid request method'})

