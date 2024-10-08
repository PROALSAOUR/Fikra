import time
from django.shortcuts import redirect, render, get_object_or_404
from accounts.forms import UserSignUpForm, UserLogInForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from store.models import Product
from accounts.models import Inbox, Message

# دالة صفحة الحساب الرئيسية
@login_required
def main_account_page(request):
    
    if request.method == 'POST' and 'logout' in request.POST: # التحقق من ضغط المستخدم على تسجيل الخروج
        logout(request)
        return redirect('store:home') # إعادة التوجيه بعد تسجيل الخروج

    
    # استدعاء المنتجات التي ستعرض اسفل الصفحة
    products = Product.objects.filter(ready_to_sale=True).order_by('updated_at')[:8]
    
    context = {
        'products' : products ,
    } 
    
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
                    login(request, user)
                    return redirect('accounts:account_page')
                else:
                    messages.error(request, "رقم الهاتف أو كلمة المرور غير صحيحة.")
        
        elif form_type == 'sign':
            sign_up_form = UserSignUpForm(request.POST or None)
            if sign_up_form.is_valid():
                new_user = sign_up_form.save()
                new_user = authenticate(username=sign_up_form.cleaned_data['phone_number'],
                                        password=sign_up_form.cleaned_data['password1'])
                if new_user:
                    login(request, new_user)
                    return redirect('store:home')
                else:
                    messages.error(request, 'فشل تسجيل الدخول بعد إنشاء الحساب.')
            
    context = {
        'sign_up_form': sign_up_form,
        'login_form': login_form,
    }     
        
    return render(request, 'accounts/sign.html', context)

# دالة عرض معلومات الحساب 
@login_required 
def account_info(request):
    user = request.user
    user_name = str(user.first_name + ' ' + user.last_name)
    phone_number = user.phone_number
    
    inbox = get_object_or_404(Inbox, user=user)
    messages = inbox.messages.all().order_by('is_read', '-timestamp')
    
    context  = {
        'user_name': user_name,
        'phone_number': phone_number,
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
#  دالة تعديل حساب
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import check_password

@login_required
def edit_account(request):
    context = {}

    if request.method == 'POST':
        # الحصول على البيانات من الفورم
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        old_password = request.POST.get('old-password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # تحقق إن كان المستخدم يرغب بتغيير الاسم فقط
        if first_name and last_name and old_password and not password1 and not password2:
            if check_password(old_password, request.user.password):
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.save()
                messages.success(request, 'تم تحديث الأسماء بنجاح.')
                return redirect('accounts:account_info')
            else:
                messages.error(request, 'كلمة المرور القديمة غير صحيحة.')

        # تحقق إن كان المستخدم يرغب بتغيير كلمة المرور فقط
        elif old_password and password1 and password2 and not first_name and not last_name:
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

        # تحقق إن كان المستخدم يرغب بتغيير الأسماء وكلمة المرور معًا
        elif first_name and last_name and old_password and password1 and password2:
            if check_password(old_password, request.user.password):
                if password1 == password2:
                    if len(password1) >= 8 and ' ' not in password1 and not password1.isdigit() and password1.isascii():
                        request.user.first_name = first_name
                        request.user.last_name = last_name
                        request.user.set_password(password1)
                        update_session_auth_hash(request, request.user)  # الحفاظ على الجلسة
                        request.user.save()
                        messages.success(request, 'تم تحديث الأسماء وكلمة المرور بنجاح.')
                        return redirect('accounts:account_info')
                    else:
                        messages.error(request, 'كلمة المرور يجب أن تكون 8 أحرف على الأقل، ولا تحتوي على فراغات، ولا تكون عبارة عن أرقام فقط.')
                else:
                    messages.error(request, 'كلمتا المرور الجديدة غير متطابقتين.')
            else:
                messages.error(request, 'كلمة المرور القديمة غير صحيحة.')

        else:
            messages.error(request, 'يرجى إدخال البيانات المطلوبة.')

    else:
        # عرض الأسماء الحالية في حالة الطلب GET
        context = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

    return render(request, 'accounts/edit.html', context)

# =============================================================







