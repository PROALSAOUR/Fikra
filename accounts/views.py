from django.shortcuts import redirect, render
from accounts.forms import UserSignUpForm, UserLogInForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from store.models import Product

@login_required
def main_account_page(request):
    
    if request.method == 'POST' and 'logout' in request.POST: # التحقق من ضغط المستخدم على تسجيل الخروج
        logout(request)
        return redirect('store:home') # إعادة التوجيه بعد تسجيل الخروج
    
    if request.user.is_authenticated : # تحقق من ان المستخدم مسجل الدخول
        pass
    else: # ان لم يمكن مسجلا حوله لصفحة التسجيل
        return redirect('accounts:sign')
    
    # استدعاء المنتجات التي ستعرض اسفل الصفحة
    points_products = Product.objects.filter(ready_to_sale=True, payment_type='points').order_by('updated_at')[:8]
    
    context = {
        'points_products' : points_products ,
    } 
    
    return render(request, 'accounts/account.html', context)


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
                first_name = sign_up_form.cleaned_data.get('first_name')
                messages.success(request, f'مرحبا {first_name} لقد انشأت حسابك بنجاح')
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
    


