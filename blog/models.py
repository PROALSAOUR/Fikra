from django.db import models

# For Blog pages in the Blog =========================

class BlogPage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True,)
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blog/pages', null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'صفحة مدونة'
        verbose_name_plural = 'صفحات المدونة '

class PageSection(models.Model):
    blog_page = models.ForeignKey(BlogPage, on_delete=models.CASCADE, related_name='sections' )
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.IntegerField(default=100)
 
    def __str__(self):
        return self.title

# For Question Page in the Blog ======================

class QuestionPage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog/questions/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'صفحة الاسئلة '
        verbose_name_plural = 'صفحة الاسئلة '
     
class QuestionContent(models.Model):
    questions_page = models.ForeignKey(QuestionPage, on_delete=models.CASCADE, related_name='questions')
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.IntegerField(default=100)

