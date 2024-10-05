from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and return a regular user with a phone number and password.
        """
        if not phone_number:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create and return a superuser with a phone number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    username = None  # حذف حقل username الأساسي
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'phone_number' 
    REQUIRED_FIELDS = ['first_name', 'last_name']  # الحقول المطلوبة عند إنشاء المستخدم

    objects = CustomUserManager()  # استخدام CustomUserManager

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'مستخدمين'
    
class Message(models.Model):
    subject = models.CharField(max_length=250)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now) 

    
    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = 'رسالة'
        verbose_name_plural = 'رسائل'

class Inbox(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='inbox')
    messages = models.ManyToManyField(Message, related_name='inboxes')

    def __str__(self):
        return f"Inbox for {self.user}"
    
    class Meta:
        verbose_name = 'البريد'
        verbose_name_plural = 'البريد'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    points = models.IntegerField(default=0)
    inbox = models.OneToOneField(Inbox, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
         
    class Meta:
        verbose_name = 'بروفايل'
        verbose_name_plural = 'بروفايل'
  
class PointsUsage(models.Model): # تتبع النقاط
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    old_points = models.IntegerField()
    new_points = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'سجل النقاط الخاص ب: {self.user_profile.user}'
         
    class Meta:
        verbose_name = 'سجل نقاط'
        verbose_name_plural = 'سجلات النقاط'
        
        
           
