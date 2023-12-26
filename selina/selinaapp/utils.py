from django.core.mail import EmailMessage
from decouple import config
import random
import string
import pyrebase

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=config('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()
  
  def generate_otp():
    otp_length = 8
    otp = ''.join(str(random.randint(0, 9)) for _ in range(otp_length))
    return otp
  
  def generate_password():
    characters = "qwertyuiopasdfghjklzxcvbnm!@#$%^&*()_+0123456789"
    new_password = ''.join(random.choice(characters) for _ in range(12))
    return new_password
  
  @staticmethod
  def upload_image(file, file_path):
    firebase = pyrebase.initialize_app({
      "apiKey": config('API_KEY'),
      "authDomain": config('AUTH_DOMAIN'),
      "projectId": config('PROJECT_ID'),
      "storageBucket": config('STORAGE_BUCKET'),
      "messagingSenderId": config('MESSAGING_SENDER_ID'),
      "appId": config('APP_ID'),
      "measurementId": config('MEASUREMENT_ID'),
      "databaseURL": ""
    })
    storage = firebase.storage()
    storage.child(file_path).put(file)
    return storage.child(file_path).get_url(None)