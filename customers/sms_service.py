import os
import africastalking
from dotenv import load_dotenv
load_dotenv()


username = os.getenv('AFRICASTALKING_USERNAME')
api_key = os.getenv('AFRICASTALKING_API_KEY')
africastalking.initialize(username, api_key)
sms = africastalking.SMS

def send_sms_notification(order):
    try:
        message = f"Hello {order.customer.name}, your order for {order.item} (Ksh {order.amount}) has been received."
        recipients = [order.customer.phone_number]
        response = sms.send(message, recipients)
        return response
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        return None