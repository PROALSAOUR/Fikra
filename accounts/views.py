from django.shortcuts import redirect, render, get_object_or_404
from accounts.forms import UserSignUpForm, UserLogInForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from store.models import Product
from accounts.models import *
from accounts.utils import send_otp_via_whatsapp, format_phone_number
from django.core.exceptions import ValidationError
import phonenumbers
from django.core.cache import cache
from settings.models import Settings

import logging
logger = logging.getLogger(__name__)  # تسجيل الأخطاء في اللوج
security_logger = logging.getLogger('django.security') # إنشاء logger للأمان

# دالة صفحة الحساب الرئيسية
@login_required
def main_account_page(request):
    if request.method == 'POST' and 'logout' in request.POST: # التحقق من ضغط المستخدم على تسجيل الخروج
        logout(request)
        return redirect('store:home') # إعادة التوجيه بعد تسجيل الخروج
    best_sales_products = cache.get('best_sales_products')
    if not best_sales_products:
        best_sales_products = Product.objects.filter(ready_to_sale=True, total_sales__gt=0).select_related('category').prefetch_related('items__variations').order_by('-total_sales')[:8]
        cache.set('best_sales_products', best_sales_products, timeout=60*60)
        
    context = {'products' : best_sales_products ,} 
    return render(request, 'accounts/account.html', context)
# دالة تسجيل الدخول و انشاء الحساب
def sign(request):
    """
    اولا تتحقق هذه الدالة من ان المستخدم غير مسجل للدخول والا تحوله الى صفحة الحساب
    ثانيا التحقق من نوع الفورم الذي ارسله المستخدم ان كان تسجيل دخول او انشاء حساب
    """
    if request.user.is_authenticated:
        return redirect('accounts:account_page')
    
    # إعداد النماذج الافتراضية
    sign_up_form = UserSignUpForm
    login_form = UserLogInForm
    if request.method == 'POST':  
        
        form_type = request.POST.get('form-type')
                  
        if form_type == 'log':
            login_form = UserLogInForm(request.POST or None)
            if login_form.is_valid():
                phone_number = login_form.cleaned_data.get('phone_number')
                password = login_form.cleaned_data.get('password')
                
                user = authenticate(request, phone_number=phone_number, password=password)
                if user is not None:
                    # تسجيل الدخول الناجح
                    login(request, user)
                    return redirect('accounts:account_page')
                else:
                    # تسجيل محاولة تسجيل دخول فاشلة
                    security_logger.warning(f'محاولة تسجيل دخول فاشلة الى حساب: : {user}')
                    messages.error(request, "رقم الهاتف أو كلمة المرور غير صحيحة.")
        
        elif form_type == 'sign':
        
            sign_up_form = UserSignUpForm(request.POST or None)
            if sign_up_form.is_valid():
                phone_number = sign_up_form.cleaned_data['phone_number']
                first_name = sign_up_form.cleaned_data['first_name']
                last_name = sign_up_form.cleaned_data['last_name']
                otp_code = OTPVerification.generate_code()

                # تحقق ان المستخدم قام بتفعيل خدمة ارسال الرسائل
                send_otp = Settings.objects.values_list('send_otp_by_twilio', flat=True).first()
                if send_otp == False :
                    messages.error(request, "المعذرة خدمة انشاء حساب تم ايقافها مؤقتا من قبل مالك الموقع يرجى المحاولة لاحقا.")
                    return redirect('accounts:sign')
            
                # إرسال OTP عبر واتساب
                formatted_phone = format_phone_number(phone_number) 
                if formatted_phone:  
                    send_otp_via_whatsapp(formatted_phone, otp_code) 
                else:
                    messages.error(request, "يرجى إدخال رقم هاتف صالح.")  

                # تخزين OTP في قاعدة البيانات
                otp_instance = OTPVerification.objects.create(
                    phone_number=phone_number ,
                    code=otp_code
                )

                request.session['otp_id'] = otp_instance.id  # تخزين الـ OTP ID في الجلسة
                request.session['phone_number'] = phone_number  # تخزين رقم الهاتف
                request.session['first_name'] = first_name  
                request.session['last_name'] = last_name 
                return redirect("accounts:verify_otp")  # الانتقال لصفحة التحقق    
            
    context = {
        'sign_up_form': sign_up_form,
        'login_form': login_form,
    }     
        
    return render(request, 'accounts/sign.html', context)
# دالة التحقق من رقم الهاتف عند انشاء حساب
def verify_otp(request):
    # اذا كان المستخدم قد سجل دخوله بالفعل اعد توجيهه لصفحة الحساب الخاص به
    if request.user.is_authenticated:
        return redirect('accounts:account_page')
    
    if request.method == "POST":
        otp_code = request.POST.get("otp_code")
        otp_id = request.session.get("otp_id")
        phone_number = request.session.get("phone_number")
        first_name = request.session.get("first_name")
        last_name = request.session.get("last_name")
        if not otp_id:
            messages.error(request, "حدث خطأ، يرجى إعادة التسجيل.")
            return redirect("accounts:sign")

        otp_instance = OTPVerification.objects.filter(id=otp_id, phone_number=phone_number).first()

        if otp_instance :
            if  otp_instance.is_valid():
                if otp_instance.code == otp_code:
                    # إنشاء الحساب بعد التحقق
                    new_user = User.objects.create_user(phone_number=phone_number, first_name=first_name , last_name=last_name)
                    login(request, new_user)
                    otp_instance.delete()# حذف الكود من قاعدة البيانات
                    del request.session['otp_id']  # حذف الكود من الجلسة
                    messages.success(request, "تم التحقق بنجاح!")
                    return redirect("accounts:choose-city")
                else:
                    otp_instance.attempts += 1
                    otp_instance.save()
                    if otp_instance.attempts >= 3:
                        messages.error(request, "لقد تجاوزت الحد الأقصى للمحاولات.")
                        return redirect("accounts:sign")
                    else:
                        messages.error(request, "رمز التحقق غير صحيح، حاول مرة أخرى.")
            else: # حذف الكود ان كان منتهي الصلاحية او جرب ادخاله اكثر من 3 مرة
                otp_instance.delete()  # حذف الكود إذا لم يكن صالحًا
                del request.session['otp_id']  # حذف الـ OTP المخزن بالجلسة
                messages.error(request, "رمز التحقق انتهت صلاحيته. حاول من جديد.")
                return redirect("accounts:sign")
        else:
            messages.error(request, "المعذرة يبدو انه قد حصل خطأ اثناء توليد رمز التحقق الخاص بك , حاول مرة اخرى لاحقا")
            return redirect("accounts:sign")

    return render(request, "accounts/verify_otp.html")
# دالة عرض معلومات الحساب 
@login_required 
def account_info(request):
    user = request.user
    user_name = str(user.first_name + ' ' + user.last_name)
    phone_number = user.phone_number
    city = user.profile.city
    
    inbox = get_object_or_404(Inbox, user=user)
    messages = inbox.messages.all().order_by('is_read', '-timestamp')[:15]
    
    context  = {
        'user_name': user_name,
        'phone_number': phone_number,
        'city': city,
        'messages': messages,
    }
    return render(request, 'accounts/account-info.html', context)
# دالة تحديث حالة الرسالة
@require_POST
def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    return JsonResponse({'status': 'success'})
# دالة حذف حساب
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # حذف المستخدم
        logout(request)  # تسجيل خروج المستخدم بعد الحذف
    return redirect('store:home')  # إعادة توجيه إلى الصفحة الرئيسية
#  دالة تعديل كلمة المرور
@login_required
def edit_account(request):    
    if request.method == 'POST':
        # الحصول على البيانات من الفورم
        old_password = request.POST.get('old-password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # تحقق إن كان المستخدم  ادخل جميع البيانات المطلوبة 
        if old_password and password1 and password2 :
            if check_password(old_password, request.user.password):
                if password1 == password2:
                    if len(password1) >= 8 and ' ' not in password1 and not password1.isdigit() and password1.isascii():
                        request.user.set_password(password1)
                        update_session_auth_hash(request, request.user)  # الحفاظ على الجلسة
                        request.user.save()
                        messages.success(request, 'تم تحديث كلمة المرور بنجاح.')
                        return redirect('accounts:account_info')
                    else:
                        messages.error(request, 'كلمة المرور يجب أن تكون 8 أحرف على الأقل، ولا تحتوي على فراغات، ولا تكون عبارة عن أرقام فقط.')
                else:
                    messages.error(request, 'كلمتا المرور الجديدة غير متطابقتين.')
            else:
                messages.error(request, 'كلمة المرور القديمة غير صحيحة.')
        else:
            messages.error(request, 'يرجى إدخال البيانات المطلوبة.')

    return render(request, 'accounts/edit-password.html')
# ================================
#  دوال تعديل كلمة المرور المنسية
def forget_password(request):
    context = {}
    # ان كان المستخدم مسجل دخوله خذ رقمه المسجل وارسل رسالة عليه
    if request.user.is_authenticated:
        phone_number = request.user.phone_number
        request.session['phone_number'] = phone_number  # تخزين رقم الهاتف
        
    else:
        # تحقق هل يوجد رقم هاتف مخزن بالجلسة ام لا ؟
        phone_number = request.session.get("phone_number")  # اذا اي جيبه وكمل
        if not phone_number:   # اذا لا روح لصفحة ادخال رقم هاتف
            return redirect('accounts:phone_number_of_forgeted_password')
            
    context.update({'phone_number': phone_number})  
            
    if request.method == 'POST':

        otp_code = OTPVerification.generate_code()
        
        # تحقق ان المستخدم قام بتفعيل خدمة ارسال الرسائل
        send_otp = Settings.objects.values_list('send_otp_by_twilio', flat=True).first()
        if send_otp == False :
            messages.error(request, "المعذرة خدمة تغيير كلمة السر تم ايقافها مؤقتا من قبل مالك الموقع يرجى المحاولة لاحقا.")
            return redirect('accounts:phone_number_of_forgeted_password')
        else:
            # إرسال OTP عبر واتساب
            formatted_phone = format_phone_number(phone_number) # الحصول على رقم الهاتف بالصيغة الدولية
            if formatted_phone:  
                send_otp_via_whatsapp(formatted_phone, otp_code)  # إرسال OTP للرقم الصحيح
            else:
                messages.error(request, "رقم الهاتف الخاص بك غير صالح ")  # إرجاع رسالة خطأ
                return redirect('accounts:edit-password')
            # تخزين OTP في قاعدة البيانات
            otp_instance = OTPVerification.objects.create(
                phone_number=phone_number, 
                code=otp_code
            )
            request.session['otp_id'] = otp_instance.id  # تخزين الـ OTP ID في الجلسة
            return redirect("accounts:verify_forget_password")  # الانتقال لصفحة التحقق   

    return render(request, 'accounts/forgot_password.html', context)
def verify_forget_password(request):
    if request.method == "POST":
        otp_code = request.POST.get("otp_code")
        otp_id = request.session.get("otp_id")
        phone_number = request.session.get("phone_number")

        if not otp_id or not phone_number:
            messages.error(request, "حدث خطأ، يرجى إعادة المحاولة لاحقاً.")
            return redirect("accounts:edit-password")

        otp_instance = OTPVerification.objects.filter(id=otp_id, phone_number=phone_number).first()

        if otp_instance :
            if  otp_instance.is_valid():
                if otp_instance.code == otp_code:
                    otp_instance.delete()# حذف الكود من قاعدة البيانات
                    del request.session['otp_id']  # حذف الكود من الجلسة
                    return redirect("accounts:reset_password") # تحويل لصفحة تغيير كلمة السر
                else:
                    otp_instance.attempts += 1
                    otp_instance.save()
                    if otp_instance.attempts >= 3:
                        messages.error(request, "لقد تجاوزت الحد الأقصى للمحاولات.")
                        return redirect("accounts:edit-password")
                    else:
                        messages.error(request, "رمز التحقق غير صحيح، حاول مرة أخرى.")
            else: # حذف الكود ان كان منتهي الصلاحية او جرب ادخاله اكثر من 3 مرة
                otp_instance.delete()  # حذف الكود إذا لم يكن صالحًا
                del request.session['otp_id']  # حذف الـ OTP المخزن بالجلسة
                messages.error(request, "رمز التحقق انتهت صلاحيته. حاول من جديد.")
                return redirect("accounts:edit-password")
        else:
            messages.error(request, "المعذرة يبدو انه قد حصل خطأ اثناء توليد رمز التحقق الخاص بك , حاول مرة اخرى لاحقا")
            return redirect("accounts:edit-password")

    return render(request, 'accounts/verify_forget_password.html')
def phone_number_of_forgeted_password(request):
    # نعمل دالة تتأكد من رقم المستخدم الي دخله انه موافق للمواصفات
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        try:
            # التحقق من صحة رقم الهاتف حسب البلد 
            parsed_phone = phonenumbers.parse(phone_number, 'LY')
            if not phonenumbers.is_valid_number(parsed_phone):
                raise ValidationError("رقم الهاتف غير صالح.")
        except phonenumbers.NumberParseException:
            raise ValidationError("يرجى إدخال رقم هاتف صحيح.")
        except Exception as e:
                logger.error(f"خطأ بدالة phone_number_of_forgeted_password: {e}", exc_info=True)
                raise ValidationError('حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا')
        # التحقق مما إذا كان الرقم مسجلاً مسبقًا
        if not User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("رقم الهاتف الذي ادخلته غير مرتبط بأي حساب  لدينا.")
        
        request.session['phone_number'] = phone_number  # تخزين رقم الهاتف
        return redirect('accounts:forget_password')  # العودة لصفحة forget_password
    
    return render(request, 'accounts/phone_number_of_forgeted_password.html')
def reset_password(request):
    if request.method == 'POST':
        phone_number =  request.session.get("phone_number")
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # تحقق من رقم الهاتف
        if not phone_number:
            logger.warning("رقم الهاتف غير موجود في الجلسة.")
            messages.error(request, 'رقم الهاتف يحتوي على خطأ')
            return redirect('accounts:forget_password') 
        
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            logger.error(f"لم يتم العثور على المستخدم برقم الهاتف: {phone_number}")
            messages.error(request, 'حدث خطأ يرجى المحاولة مرة أخرى أو التواصل مع الدعم في حال استمرت المشكلة')
            return redirect('accounts:forget_password')
        except Exception as e:
            logger.error(f"خطأ ب: {e}", exc_info=True)
            messages.error(request, 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقًا')
            return redirect('accounts:forget_password')
        
        # تحقق من كلمات السر 
        if not password1 or not password2 or password1 != password2:
            messages.error(request, '!كلمات السر غير متطابقة .')
            return redirect('accounts:reset_password')
        if len(password1) >= 8 and ' ' not in password1 and not password1.isdigit() and password1.isascii():
            request.session.pop("phone_number", None)  # حذف الـرقم المخزن بالجلسة
            if request.user.is_authenticated:
                request.user.set_password(password1)
                update_session_auth_hash(request, request.user)  # الحفاظ على الجلسة
                request.user.save()
                messages.success(request, 'تم تحديث كلمة المرور بنجاح.')
                return redirect('accounts:account_info')
            else: # لو المستخدم عم يغير كلمة السر وهو مو مسجل, غيرها بعدين خليه يسجل دخول على حسابه
                user.set_password(password1)
                user.save()
                login(request, user)  
                return redirect('accounts:account_info') 
        else:
            messages.error(request, 'كلمة المرور يجب أن تكون 8 أحرف على الأقل، ولا تحتوي على فراغات، ولا تكون عبارة عن أرقام فقط.')
            return redirect('accounts:reset_password')
        
    return render(request, 'accounts/reset_password.html')
# ================================
# دالة تعديل اسم المستخدم
@login_required
def edit_name(request):    
    context = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
    }
    if request.method == 'POST':
        # الحصول على البيانات من الفورم
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')

        if first_name and last_name :
            if ' ' in first_name or ' ' in last_name:
                messages.error(request, 'لايمكن استخدام المسافات داخل الاسماء!')
            else:
                # تحقق انه لم يقم بإدخال نفس الاسم القديم
                if request.user.first_name!= first_name or request.user.last_name!= last_name:
                    request.user.first_name = first_name
                    request.user.last_name = last_name
                    request.user.save()
                    messages.success(request, 'تم تحديث الأسماء بنجاح.')
                    return redirect('accounts:account_info')    
                else:
                    messages.error(request, 'الأسماء الحالية مطابقة للأسماء القديمة!.')
        else:
            messages.error(request, 'يرجى إدخال البيانات المطلوبة.')
    return render(request, 'accounts/edit-name.html', context)
# =============================================================
# دالة اختيار المدينة
@login_required
def choose_city(request):
    context = {}
    user = request.user
    user_city = user.profile.city if user.profile.city else None
    
    if request.method == 'POST':
        selected_city_name = request.POST.get('city')  # الحصول على المدينة المختارة
        if selected_city_name:
            try:
                # البحث عن المدينة باستخدام الاسم
                selected_city = City.objects.get(name=selected_city_name)
                user.profile.city = selected_city  # تعيين كائن City
                user.profile.save()
                messages.success(request, 'تم تحديث المدينة الحالية بنجاح')
                return redirect('accounts:account_info')
            except City.DoesNotExist:
                messages.error(request, 'المدينة غير موجودة.')
            except Exception as e :
                logger.error(f"خطأ بالبحث عن المدينة: {e}", exc_info=True)
                messages.error(request, 'حدث خطأ غير متوقع، الرجاء المحاولة لاحقاً')
                return redirect('accounts:choose_city') 
    else:
        cites = City.objects.all()
        context = {
            'user_city': user_city,
            'cites': cites,
        }
        
    return render(request, 'accounts/choose-city.html', context)
