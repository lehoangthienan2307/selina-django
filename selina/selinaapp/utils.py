from django.core.mail import EmailMessage
from decouple import config
import random
import string
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