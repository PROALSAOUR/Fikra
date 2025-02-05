from twilio.rest import Client
from django.conf import settings
import phonenumbers


def send_otp_via_whatsapp(phone_number, otp_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"رمز التحقق الخاص بحسابك على موقع فكرة هو: {otp_code}",
        from_=f"{settings.TWILIO_WHATSAPP_NUMBER}",
        to=f"whatsapp:{phone_number}"
    )
    return message.sid

def format_phone_number(phone_number):
    """
    يحوّل رقم الهاتف إلى الصيغة الدولية E.164 إذا لم يكن دوليًا بالفعل.
    """
    try:
        # تحليل الرقم بدون تحديد الدولة، كي يتعرف على المقدمة الدولية إن وجدت
        parsed_phone = phonenumbers.parse(phone_number, None)  

        # إذا كان الرقم صالحًا ومعترفًا به دوليًا، نعيده كما هو
        if phonenumbers.is_valid_number(parsed_phone):
            return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
        
    except phonenumbers.NumberParseException:
        pass  # فشل التحليل، سنحاول إضافته كرقم ليبي

    # إذا لم يكن الرقم دوليًا، نعامله كرقم ليبي
    try:
        parsed_phone = phonenumbers.parse(phone_number, "LY")  
        if phonenumbers.is_valid_number(parsed_phone):
            return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return None  # الرقم غير صالح بأي حال

    return None  # إذا لم يكن الرقم صالحًا


