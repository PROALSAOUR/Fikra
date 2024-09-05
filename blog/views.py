from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.

def blog(request):
    blog_pages = BlogPage.objects.all().order_by('order')
    questions_page = QuestionPage.objects.first()
      
    context = {
        'blog_pages': blog_pages,
        'questions_page': questions_page,
    }
    
    return render(request, 'blog/blog.html', context)

def page_details(request, slug):
    # جلب الصفحة المحددة أو إظهار خطأ 404 إذا لم يتم العثور عليها
    blog_page = get_object_or_404(BlogPage, slug=slug)
    
    context = {
        'blog_page': blog_page,
        'sections': blog_page.sections.all().order_by('order'),
    }
    return render(request, 'blog/blog-page.html', context)

def questions_page(request):
    questions_page = QuestionPage.objects.first()
    
    context = {
        'questions_page': questions_page,
        'questions': questions_page.questions.all().order_by('order')  # الحصول على الأقسام المرتبطة,
    }
    return render(request, 'blog/questions-page.html', context)
