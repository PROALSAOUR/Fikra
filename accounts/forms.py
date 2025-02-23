from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
import phonenumbers

import logging
logger = logging.getLogger(__name__)  # تسجيل الأخطاء في اللوج

class UserSignUpForm(UserCreationForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':"user-first-name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':"user-last-name"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'id':'user-phone'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'passoword1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'passoword2'}))
    otp_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'id': 'otp-code'}),
        help_text="سيتم إرسال رمز التحقق إلى رقم واتساب الخاص بك."
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'otp_code']
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            # التحقق من صحة رقم الهاتف حسب البلد 
            parsed_phone = phonenumbers.parse(phone_number, 'LY')
            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValidationError("رقم الهاتف غير صالح.")
        except phonenumbers.NumberParseException:
            raise ValidationError("يرجى إدخال رقم هاتف صحيح.")
        except Exception as e:
            logger.error(f"خطأ داخل نموذج انشاء حساب: {e}", exc_info=True)
            raise ValidationError( 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا')
        
        # التحقق مما إذا كان الرقم مسجلاً مسبقًا
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("رقم الهاتف مستخدم بالفعل. يرجى تسجيل الدخول بدلاً من ذلك.")
        return phone_number
    
class UserLogInForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get('password')
        
        user = authenticate(phone_number=phone_number, password=password)
        if user is None:
            raise forms.ValidationError("رقم الهاتف أو كلمة المرور غير صحيحة.")
        return self.cleaned_data
    
