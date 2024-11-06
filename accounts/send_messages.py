from django.utils import timezone
from accounts.models import Message


def copon_expire_after_3_dayes(user_name, copon_name):
    """ نص رسالة متبقي 3 ايام على انتهاء صلاحية الكوبون"""
    message = Message(
        subject= 'صلاحية احد كوبوناتك على وشك الانتهاء!',
        content= 
        f"""
        مرحبا {user_name}, 
        نود تنبيهك ان الكوبون ( {copon_name} )  الخاص بك ستنتهي صلاحيته بعد ثلاثة ايام من تاريخ اليوم , لذلك حاول استعماله قريبا لتجنب خسارته. 
        في حال كان لديك اي استفسار لا تتردد بالتواصل معنا.
        """,
        timestamp=timezone.now()
    ) 
    message.save()
    return message 

def copon_expire_today(user_name, copon_name):
    """نص رسالة انتهاء صلاحية الكوبون"""
    
    message = Message(
        subject= 'لقد انتهت صلاحية احد الكوبونات الخاصة بك',
        content= 
        f"""
        مرحبا {user_name}, 
        نود تنبيهك ان الكوبون ( {copon_name} )  الخاص بك قد انتهت صلاحيته وسوف يتوجب عليك شراؤه مرة اخرى كي تتمكن من استعماله , شاكرين لك حسن تفهمك. 
        في حال كان لديك اي استفسار لا تتردد بالتواصل معنا.
        """,
        timestamp=timezone.now()
    ) 
    message.save()
    return message 

def wellcome_new_user(user_name):
    """نص الرسالة التي ترسل للمستخدم عند انشاء حساب"""
    message = Message(
            subject= f'اهلا بك في فكرة',
            content= 
            f"""
            مرحبا {user_name}
            ,لا يسعنا وصف سعادتنا بإنضمامك الى عائلة فكرة , نرجو ان نكون عند حسن ظنك و ان نقدم لك تجربة تسوق استثنائية و مميزة,
            في حال كان لديك اي استفسار لا تتردد بالتواصل معنا
            """,
            timestamp=timezone.now()
            )
    message.save()
    return message

def message_when_buy_gift_for_me(user_name, gift_name):
    """الرسالة التي ترسل عند شراء هدية  لنفسي"""

    message = Message(
        subject= f'تمت عملية شراء الهدية بنجاح',
        content= 
        f"""
        مرحبا {user_name}
        لقد تمت عملية شراء الهدية ({ gift_name }) بنجاح يمكنك العثور عليها الأن داخل مخزونك واستعمالها مع احد طلباتك القادمة ,
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def receiver_gift_message(recipient_name, buyer_name, gift_name):
    """الرسالة التي ترسل الى المستلم عندما يرسل اليه احدهم هدية"""
    message = Message(
        subject= f' ارسل احدهم هدية اليك!',
        content= 
        f"""
        مرحبا {recipient_name}
        لقد قام {buyer_name} بإرسال هدية [{ gift_name }]  ,اليك, يمكنك الاطلاع عليها الأن داخل مخزون البطاقات الخاص بك و استعمالها مع اي طلب تريده
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def sender_gift_message(user_name, receiver_name, gift_name):
    """الرسالة التي ترسل الى المستخدم عندما يقوم  بإرسال هدية الى احدهم   """
    message = Message(
        subject= f'تم ارسال الهدية بنجاح!',
        content= 
        f"""
        مرحبا {user_name}
        لقد تم شراء الهدية ( {gift_name} ) و ارسالها الى ( {receiver_name} ) بنجاح , 
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def buy_copon_done_message(user_name, copon_name):
    """الرسالة التي ترسل للمستخدم عند شراء كوبون"""

    message = Message(
        subject= f'تمت عملية شراء كوبون بنجاح',
        content= 
        f"""
        مرحبا {user_name}
        لقد تمت عملية شراء الكوبون ({ copon_name }) بنجاح يمكنك العثور عليه الأن داخل مخزونك واستعماله مع احد طلباتك القادمة ,
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )    
    message.save()
    return message

def send_gift_to_someone_not_in_fikra(user_name, gift, recipient_name, recipient_phone):
    """الرسالة التي ترسل الى المستخدم  عندما يرسل هدية لشخص ليس لديه حساب على فكرة"""
    # رسالة الى المشتري تخبره ان المستلم ليس لديه حساب على فكرة وانه سيتم التواصل معه
    message = Message(
        subject= f'تمت عملية شراء الهدية بنجاح',
        content= 
        f"""
        مرحبا {user_name}
        لقد تمت عملية شراء الهدية ({ gift }) بنجاح, يبدو ان  ({recipient_name}[{recipient_phone}]) غير مسجل في قاعدة البيانات الخاصة بمتجرنا لكن لاتقلق سوف يتواصل معه احد موظفينا لإيصال هديتك اليه,
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def add_order_points_message(order_se, user_name, points):
    """الرسالة التي ترسل الى المستخدم عنما يستلم الطلب الخاص به تفيد بأنه تم اضافة النقاط الى حسابه"""
    message = Message(
            subject= f'تم اضافة نقاط الطلب [{str(order_se).zfill(6)}] !',
            content= 
            f"""
            مرحبا {user_name} 
            لقد تمت اضافة النقاط التابعة للطلب [{str(order_se).zfill(6)}] والتي قيمتها {points} نقطة بنجاح الى حسابك, 
            نرجو لك وقتا سعيداً.
            """,
            timestamp=timezone.now()
            )
    message.save()
    return message

def create_order_message(user_name, order):
    """الرسالة التي ترسل عند انشاء طلب جديد"""
    message = Message(
        subject= f'طلبك في طريقه اليك!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم انشاء الطلب ({str(order).zfill(6)}) بنجاح, سوف نقوم بإرساله اليك خلال مدة لا تتجاوز ال 3 أيام.\n 
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن\n
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def cancel_order_message(user_name, order):
    """الرسالة التي ترسل عند إلغاء طلب """
    message = Message(
        subject= f'تم إلغاء الطلب بنجاح!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم إلغاء الطلب ({str(order).zfill(6)}) بنجاح .\n 
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن\n
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def edit_order_message(user_name, order):
    """الرسالة التي ترسل عند تعديل طلب """
    message = Message(
        subject= f'تم تعديل الطلب بنجاح!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم تعديل الطلب ({str(order).zfill(6)}) الخاص بك بنجاح سوق يتواصل معك مندوب التوصيل الخاص بنا قريبا, شاكرين لك حسن تفهمك.\n 
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن\n
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message
    
def return_order_item_message(user_name, order):
    """الرسالة التي ترسل عند ارجاع منتج من طلب """
    message = Message(
        subject= f'تم إنشاء طلب إرجاع بنجاح!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم انشاء طلب إرجاع لأحد المنتجات التابعة  للطلب ({str(order).zfill(6)}) الخاص بك بنجاح سوق يتواصل معك مندوب التوصيل الخاص بنا قريبا, شاكرين لك حسن تفهمك.\n 
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن\n
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message
    



