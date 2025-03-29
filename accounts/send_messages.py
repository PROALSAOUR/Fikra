from django.utils import timezone
from accounts.models import Message
from settings.models import Settings
from django.urls import reverse


def copon_expire_after_3_dayes(user_name, copon_name):
    """ نص رسالة متبقي 3 ايام على انتهاء صلاحية الكوبون"""
    repo_url = reverse("cards:cards-repo")
    message = Message(
        subject= 'صلاحية احد كوبوناتك على وشك الانتهاء!',
        content= 
        f"""
        مرحبا {user_name}, 
        نود تنبيهك ان الكوبون ( {copon_name} )  الخاص بك ستنتهي صلاحيته بعد ثلاثة ايام من تاريخ اليوم , لذلك حاول استعماله قريبا لتجنب خسارته. 
        في حال كان لديك اي استفسار لا تتردد بالتواصل معنا.
        <br><a href="{repo_url}">عرض مخزون البطاقات الخاص بي</a>
        """,
        timestamp=timezone.now()
    ) 
    message.save()
    return message 

def copon_expired_today(user_name, copon_name):
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

def buy_copon_done_message(user_name, copon_name):
    """الرسالة التي ترسل للمستخدم عند شراء كوبون"""
    repo_url = reverse("cards:cards-repo")
    message = Message(
        subject= f'تمت عملية شراء كوبون بنجاح',
        content= 
        f"""
        مرحبا {user_name}
        لقد تمت عملية شراء الكوبون ({ copon_name }) بنجاح يمكنك العثور عليه الأن داخل <a href="{repo_url}">مستودع بطاقاتك</a> واستعماله مع احد طلباتك القادمة ,
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )    
    message.save()
    return message

def receive_copon_done_message(user_name, copon_name):
    """الرسالة التي ترسل للمستخدم عند استلام كوبون بواسطة الكود"""
    repo_url = reverse("cards:cards-repo")
    message = Message(
        subject= f'تمت عملية استلام الكوبون بنجاح',
        content= 
        f"""
        مرحبا {user_name}
        لقد تمت عملية استلام الكوبون ({ copon_name }) بنجاح يمكنك العثور عليه الأن داخل <a href="{repo_url}">مستودع بطاقاتك</a> واستعماله مع احد طلباتك القادمة ,
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
        """,
        timestamp=timezone.now()
    )    
    message.save()
    return message

def add_order_points_message(order, user_name, points):
    """الرسالة التي ترسل الى المستخدم عنما يستلم الطلب الخاص به تفيد بأنه تم اضافة النقاط الى حسابه"""
    order_url = reverse("orders:order-details", kwargs={"oid": order.id})
    message = Message(
        subject= f'تم اضافة نقاط الطلب ({str(order.serial_number).zfill(6)}) !',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تمت اضافة النقاط التابعة للطلب (<a href='{order_url}'>{str(order.serial_number).zfill(6)}</a>) والتي قيمتها {points} نقطة بنجاح الى حسابك, <br> 
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def create_order_message(user_name, order):
    """الرسالة التي ترسل عند انشاء طلب جديد"""
    order_url = reverse("orders:order-details", kwargs={"oid": order.id})
    message = Message(
        subject= f'طلبك في طريقه اليك!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم انشاء الطلب (<a href='{order_url}'>{str(order.serial_number).zfill(6)}</a>) بنجاح, سوف نقوم بإرساله اليك خلال مدة لا تتجاوز ال {Settings.objects.first().expected_days} أيام.<br>
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن<br>
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def cancel_order_message(user_name, order):
    """الرسالة التي ترسل عند إلغاء طلب """
    order_url = reverse("orders:order-details", kwargs={"oid": order.id})
    message = Message(
        subject= f'تم إلغاء الطلب بنجاح!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم إلغاء الطلب (<a href='{order_url}'>{str(order.serial_number).zfill(6)}</a>) بنجاح .<br>
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن<br>
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message

def edit_order_message(user_name, order):
    """الرسالة التي ترسل عند تعديل طلب """
    order_url = reverse("orders:order-details", kwargs={"oid": order.id})
    message = Message(
        subject= f'تم تعديل الطلب بنجاح!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم تعديل الطلب (<a href='{order_url}'>{str(order.serial_number).zfill(6)}</a>) الخاص بك بنجاح سوق يتواصل معك مندوب التوصيل الخاص بنا قريبا, شاكرين لك حسن تفهمك.\n 
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن<br>
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message
    
def return_order_item_message(user_name, order):
    """الرسالة التي ترسل عند ارجاع منتج من طلب """
    order_url = reverse("orders:order-details", kwargs={"oid": order.id})
    message = Message(
        subject= f'تم إنشاء طلب إرجاع بنجاح!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد تم انشاء طلب إرجاع لأحد المنتجات التابعة  للطلب (<a href='{order_url}'>{str(order.serial_number).zfill(6)}</a>) الخاص بك بنجاح سوق يتواصل معك مندوب التوصيل الخاص بنا قريبا, شاكرين لك حسن تفهمك.\n 
        في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن<br>
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message
    
def user_got_blocked(user_name):
    """الرسالة التي ترسل عند حظر مستخدم """
    message = Message(
        subject= f'تم حظر حسابك!',
        content= 
        f"""
        مرحبا {user_name} 
        لقد لاحظنا قيامك ببعض النشاطات المخالفة لسياسات متجرنا لذا اضطررنا لتقييد حسابك،
        في حال كنت تعتقد انك لم تقم بأي مخالفات يرجى التواصل مع خدمة العملاء وسوف يتم مراجعة نشاطات حسابك <br>
        نرجو لك وقتا سعيداً.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message
    
def send_message_to_user_when_product_available(user_name, product_name, product_id):
    """الرسالة التي ترسل الى المستخدم لإعلامه ان المنتج اصبح متوفر  """
    product_url = reverse("store:product_details", kwargs={"pid": product_id})
    message = Message(
        subject= f'تم توفير كمية جديدة من {product_name}',
        content= 
        f"""
        مرحبا {user_name} 
        لقد قمنا بتوفير المنتج <a href="{product_url}" aria-label="استعرض {product_name}">{product_name}</a> الذي كنت مهتمًا به حيث أصبح متاحًا الآن للشراء.
        """,
        timestamp=timezone.now()
    )
    message.save()
    return message
