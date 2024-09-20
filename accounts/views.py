from django.shortcuts import redirect, render, get_object_or_404
from accounts.forms import UserSignUpForm, UserLogInForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
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
    points_products = Product.objects.filter(ready_to_sale=True, payment_type='points').order_by('updated_at')[:8]
    
    context = {
        'points_products' : points_products ,
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

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # حذف المستخدم
        logout(request)  # تسجيل خروج المستخدم بعد الحذف
    return redirect('store:home')  # إعادة توجيه إلى الصفحة الرئيسية