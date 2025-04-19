
import os
import africastalking
from dotenv import load_dotenv
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def initialize_africastalking():
    """Initialize Africa's Talking SDK with validation"""
    username = os.getenv('AFRICASTALKING_USERNAME')
    api_key = os.getenv('AFRICASTALKING_API_KEY')
    
    if not username or not api_key:
        logger.error("Africa's Talking credentials not configured in environment variables")
        raise ValueError("Missing Africa's Talking credentials")
    
    try:
        africastalking.initialize(username, api_key)
        return africastalking.SMS
    except Exception as e:
        logger.error(f"Failed to initialize Africa's Talking: {str(e)}")
        raise

# Initialize once when module loads
try:
    sms = initialize_africastalking()
except Exception as e:
    sms = None
    logger.warning(f"Africa's Talking not available: {str(e)}")

def format_phone_number(phone_number):
    """Format phone number to E.164 format (+254...)"""
    # Remove all non-digit characters
    digits = re.sub(r'[^\d]', '', phone_number)
    
    # Handle Kenyan numbers
    if digits.startswith('0') and len(digits) == 9:
        return f"+254{digits[1:]}"
    elif digits.startswith('254') and len(digits) == 12:
        return f"+{digits}"
    elif digits.startswith('7') and len(digits) == 9:
        return f"+254{digits}"
    
    # Return as-is if already in E.164 format
    if digits.startswith('+254') and len(digits) == 13:
        return digits
    
    raise ValueError(f"Invalid phone number format: {phone_number}")

def send_sms_notification(order):
    """
    Send SMS notification for a new order
    Returns tuple: (success: bool, response: dict|str)
    """
    if sms is None:
        error_msg = "Africa's Talking not initialized - SMS not sent"
        logger.error(error_msg)
        return False, error_msg
    
    try:
        # Validate and format phone number
        formatted_phone = format_phone_number(order.customer.phone_number)
        
        # Create message
        message = f"Hello {order.customer.name}, your order for {order.item} (Ksh {order.amount}) has been received."
        
        # Send SMS
        response = sms.send(message, [formatted_phone])
        logger.info(f"SMS sent to {formatted_phone}. Response: {response}")
        
        # Check if successfully sent
        if (response['SMSMessageData']['Recipients'][0]['statusCode'] in [101, 102]):
            return True, response
        else:
            error_msg = f"SMS failed with status: {response['SMSMessageData']['Recipients'][0]['status']}"
            logger.error(error_msg)
            return False, error_msg
            
    except ValueError as e:
        logger.error(f"Invalid phone number: {str(e)}")
        return False, str(e)
    except Exception as e:
        logger.error(f"Failed to send SMS: {str(e)}")
        return False, str(e)

