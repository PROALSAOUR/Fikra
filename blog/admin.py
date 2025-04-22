from django.contrib import admin
from .models import BlogPage, PageSection, QuestionPage, QuestionContent

class PageSectionInline(admin.TabularInline): 
    model = PageSection
    fields = ('title', 'content', 'order')  # الحقول التي تريد عرضها في واجهة الإدارة
    ordering = ('order',)  # ترتيب الحقول حسب القيمة الافتراضية لـ 'order'
    extra = 0 

class BlogPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title',)
    list_filter = ('order',)
    ordering = ('order',)
    inlines = [PageSectionInline]  # إضافة الـ InlineModelAdmin هنا

class QuestionContentInline(admin.TabularInline):  
    model = QuestionContent
    fields = ('slug', 'title','content', 'order') 
    ordering = ('order',)  # ترتيب الحقول حسب القيمة الافتراضية لـ 'order'
    extra = 0 

class QuestionPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [QuestionContentInline] 
    
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not QuestionPage.objects.exists()
    
admin.site.register(QuestionPage, QuestionPageAdmin)
admin.site.register(BlogPage, BlogPageAdmin)
