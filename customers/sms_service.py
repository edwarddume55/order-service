import os
import africastalking
from dotenv import load_dotenv
import logging
import re
import ssl
from urllib3.util.ssl_ import create_urllib3_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

class SMSService:
    def __init__(self, sandbox=False):
        self.sms = None
        self.sandbox = sandbox
        self._patch_ssl() 
        self.initialize()
    
    def _patch_ssl(self):
        """Workaround for SSL/TLS compatibility issues"""
        ctx = create_urllib3_context()
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        ssl._create_default_https_context = lambda: ctx
    
    def initialize(self):
        username = os.getenv('AFRICASTALKING_USERNAME', 'sandbox')
        api_key = os.getenv('AFRICASTALKING_API_KEY')
        
        if not api_key:
            raise ValueError("API key required (set AFRICASTALKING_API_KEY)")
            
        africastalking.initialize(username, api_key)
        self.sms = africastalking.SMS
        self.sms.sandbox = self.sandbox
        
    @staticmethod
    def format_phone_number(phone_number):
        digits = re.sub(r'[^\d]', '', phone_number)
        if not digits or len(digits) < 9:
            raise ValueError("Invalid number length")
            
        if digits.startswith('0') and len(digits) == 10:
            return f"+254{digits[1:]}"
        elif digits.startswith('7') and len(digits) == 9:
            return f"+254{digits}"
        elif digits.startswith('254') and len(digits) == 12:
            return f"+{digits}"
        elif digits.startswith('+254'):
            return digits
        raise ValueError(f"Invalid format: {phone_number}")

    def send_sms_notification(self, order):
        try:
            phone = self.format_phone_number(order.customer.phone_number)
            msg = f"Hello {order.customer.name}, your order of {order.item}, have been received.."
            
            print(f"\n📲 Sending to {phone}: {msg[:30]}...")
            response = self.sms.send(msg, [phone])
            
            status = response['SMSMessageData']['Recipients'][0]['statusCode']
            if status == 101:
                print("SMS Sent successfully!")
            else:
                print(f"Failed! Status: {status}")
            return (status == 101), response
            
        except Exception as e:
            logger.error(f"SMS Error: {e}", exc_info=True)
            return False, str(e)

#sandbox mode by default
sms_service = SMSService(sandbox=True)