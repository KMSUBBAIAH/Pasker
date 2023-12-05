import requests
from django.urls import reverse
# from .rfid_authenticate import get_auth_id

import serial
import requests
from django.urls import reverse
import warnings
warnings.filterwarnings('ignore')

def get_auth_id():
    arduino = serial.Serial('COM3',9600)
    # print("Established Connection:")
    while(True):
        data = arduino.readline()
        decode_val = str(data[0:len(data)].decode(encoding='utf-8'))
        # print(decode_val)
        return decode_val
    # return '236A3AFA'

# def read_rfid_and_send_to_django():
#     rfid_value = get_auth_id()  # Get RFID ID from the RFID reader
#     print(rfid_value)
#     # Get the CSRF token from the Django server
#     # Get the CSRF token from the Django server
#     # csrf_url = 'http://127.0.0.1:8000/get_csrf_token'  # Use the new URL pattern
#     # csrf_response = requests.get(csrf_url)

#     # if csrf_response.status_code == 200:
#     #     csrf_token = csrf_response.json().get('csrf_token')
#     # else:
#     #     print("Error getting CSRF token.")
#     #     return

#     # Send the RFID ID to your Django registration view
#     url = 'http://127.0.0.1:8000/authentication/'
#     # url = reverse('authentication')  # Update with your Django URL
#     data = {'authentication_id': rfid_value}  # Assuming 'authentication_id' is the form field name
#     response = requests.post(url, data=data)

#     if response.status_code == 200:
#         print("RFID ID sent to Django successfully.")
#     else:
#         print("Error sending RFID ID to Django.")


def main():
    get_auth_id()

if __name__ == '__main__':
    main()