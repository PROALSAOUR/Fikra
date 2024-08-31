from django.contrib import admin
from .models import BlogPage, PageSection, QuestionPage, QuestionContent

# الشيفرة الخاصة بصفحات المحتوى

class PageSectionInline(admin.TabularInline): 
    model = PageSection
    extra = 1  # عدد النماذج الفارغة التي سيتم عرضها بشكل افتراضي
    fields = ('title', 'content', 'order')  # الحقول التي تريد عرضها في واجهة الإدارة
    ordering = ('order',)  # ترتيب الحقول حسب القيمة الافتراضية لـ 'order'

@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title',)
    list_filter = ('order',)
    ordering = ('order',)
    inlines = [PageSectionInline]  # إضافة الـ InlineModelAdmin هنا

# الشيفرة الخاصة بصفحة الاسئلة

class QuestionContentInline(admin.TabularInline):  # أو admin.StackedInline
    model = QuestionContent
    extra = 1 
    fields = ('title', 'content', 'order')  # الحقول التي تريد عرضها في واجهة الإدارة
    ordering = ('order',)  # ترتيب الحقول حسب القيمة الافتراضية لـ 'order'

@admin.register(QuestionPage)
class QuestionPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [QuestionContentInline] 
    
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not QuestionPage.objects.exists()
    

