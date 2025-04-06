from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# For Blog pages in the Blog =========================

class BlogPage(models.Model):
    title = models.CharField(max_length=100, verbose_name='العنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    order = models.IntegerField(default=0, verbose_name='الترتيب')
    image = models.ImageField(upload_to='blog/pages', null=True, blank=True , verbose_name='الخلفية')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'صفحة مدونة'
        verbose_name_plural = 'صفحات المدونة '

class PageSection(models.Model):
    blog_page = models.ForeignKey(BlogPage, on_delete=models.CASCADE, related_name='sections', verbose_name='الصفحة' )
    title = models.CharField(max_length=255, verbose_name='العنوان')
    content = CKEditor5Field('المحتوى', config_name='default')
    order = models.IntegerField(default=100 , verbose_name='الترتيب')
 
    def __str__(self):
        return self.title

# For Question Page in the Blog ======================

class QuestionPage(models.Model):
    title = models.CharField(max_length=100 , verbose_name='العنوان')
    image = models.ImageField(upload_to='blog/questions/', null=True, blank=True, verbose_name='الخلفية')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'صفحة الاسئلة '
        verbose_name_plural = 'صفحة الاسئلة '
     
class QuestionContent(models.Model):
    questions_page = models.ForeignKey(QuestionPage, on_delete=models.CASCADE, related_name='questions', verbose_name='الصفحة')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    content = CKEditor5Field('المحتوى', config_name='default')
    order = models.IntegerField(default=100, verbose_name='الترتيب')

