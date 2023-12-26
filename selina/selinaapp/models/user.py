from selina.models.timestamp import TimeStampModel
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone, gender, type, password=None, password2=None):

        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            phone=phone,
            gender=gender,
            user_type=type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, phone, gender, password=None):

        user = self.create_user(
            email,
            fullname=fullname,
            phone=phone,
            gender=gender,
            password = password
        )
        user.user_type = 'admin'
        user.save(using=self._db)
        return user

class User(TimeStampModel, AbstractUser):
    username = None
    first_name = None
    last_name = None

    class Meta:
        db_table = 'user_information'
        app_label = "selinaapp"
        
    class Gender(models.IntegerChoices):
        FEMALE = 0
        MALE = 1
        OTHER = 2
    
    class Status(models.TextChoices):
        REJECTED = "rejected"
        APPROVED = "approved"
        PENDING = "pending"

    class Type(models.TextChoices):
        NORMAL_USER = "normal_user"
        SELLER = "seller"
        ADMIN = "admin"

    objects = UserManager()

   # id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=20, null=True, default=None, blank=True)
    email = models.EmailField(max_length=255, unique=True)
   # password = models.BinaryField(blank=False, null=False)
    device_token = models.CharField(max_length=1000, null=True, default=None)
    avatar_url = models.CharField(max_length=1000, null=False, blank=True, default='')
    user_type = models.CharField(max_length=255, null=True, choices=Type.choices, default=Type.NORMAL_USER)
    status = models.CharField(max_length=255, null=True, choices=Status.choices, default=Status.PENDING)
    gender = models.SmallIntegerField(choices=Gender.choices, default=Gender.OTHER)
    address = models.CharField(max_length=255, null=True, default=None)

    #TO DO: change to redis
    otp = models.CharField(max_length=8, null=True, default=None)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
            return self.email