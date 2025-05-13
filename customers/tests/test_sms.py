import pytest
from unittest.mock import patch, MagicMock
from customers.sms_service import SMSService, sms_service

@patch.dict('os.environ', {
    'AFRICASTALKING_USERNAME': 'testuser',
    'AFRICASTALKING_API_KEY': 'testkey'
})
@patch('customers.sms_service.africastalking.initialize')
@patch('customers.sms_service.africastalking.SMS', autospec=True)
def test_initialize_africastalking_success(mock_sms, mock_initialize):
    """Test successful initialization of Africa's Talking SMS service"""
    service = SMSService()
    mock_initialize.assert_called_once_with('testuser', 'testkey')
    assert service.sms == mock_sms

@pytest.mark.parametrize("input_phone,expected", [
    ("0722123456", "+254722123456"),
    ("722123456", "+254722123456"),
    ("254722123456", "+254722123456"),
    ("+254722123456", "+254722123456")
])
def test_format_phone_number_valid(input_phone, expected):
    """Test valid phone number formatting"""
    assert SMSService.format_phone_number(input_phone) == expected

def test_format_phone_number_invalid():
    """Test invalid phone number raises ValueError"""
    with pytest.raises(ValueError):
        SMSService.format_phone_number("12345")
    with pytest.raises(ValueError):
        SMSService.format_phone_number("0722123456789")

def test_send_sms_notification_success():
    """Test successful SMS notification"""
    # Setup mock
    with patch.object(sms_service, 'sms') as mock_sms:
        mock_sms.send.return_value = {
            'SMSMessageData': {
                'Recipients': [{
                    'statusCode': 101,
                    'status': 'Success',
                    'number': '+254722123456'
                }],
                'Message': 'Sent to 1/1'
            }
        }

        # Create mock order
        mock_order = MagicMock()
        mock_order.customer.phone_number = "0722123456"
        mock_order.customer.name = "Alice"
        mock_order.item = "Laptop"
        mock_order.amount = 10000

        success, response = sms_service.send_sms_notification(mock_order)
        
        assert success is True
        assert 'SMSMessageData' in response
        mock_sms.send.assert_called_once()

def test_send_sms_notification_failure():
    """Test failed SMS notification"""
    # Setup mock
    with patch.object(sms_service, 'sms') as mock_sms:
        mock_sms.send.return_value = {
            'SMSMessageData': {
                'Recipients': [{
                    'statusCode': 400,
                    'status': 'Invalid Number',
                    'number': '+254722123456'
                }],
                'Message': 'Failed to send'
            }
        }

        # Create mock order
        mock_order = MagicMock()
        mock_order.customer.phone_number = "0722123456"
        mock_order.customer.name = "Bob"
        mock_order.item = "Phone"
        mock_order.amount = 3000

        success, response = sms_service.send_sms_notification(mock_order)
        
        assert success is False
        assert "failed" in str(response).lower()
        mock_sms.send.assert_called_once()