from django.test import TestCase
from ippanel import HTTPError, Error, ResponseCode
from ippanel import Client

api_key = "1o2dzyt4MHJUJrqDRzdvZiRc3pvDYPZ0p8vxCLKJUbI="


LOGIN_VERIFICATION = 's7n0wwywngv2zud'
ORDER_SUBMITED = '2lbj39z83uqgz9c'
OWNER_ORDER_NOTIFICATION = 'qa3beq00ab2ug2c'


def send_sms(pattern, recipient, **kwargs):
    try:
        sms = Client(api_key)
        message_id = sms.send_pattern(
            pattern,  # pattern code
            "3000505",  # originator
            recipient,  # recipient
            kwargs,  # pattern values
        )
    except Error as e:  # ippanel sms error
        print(f"Error handled => code: {e.code}, message: {e.message}")
        if e.code == ResponseCode.ErrUnprocessableEntity.value:
            for field in e.message:
                print(f"Field: {field} , Errors: {e.message[field]}")
    except HTTPError as e:  # http error like network error, not found, ...
        print(f"Error handled => code: {e}")
