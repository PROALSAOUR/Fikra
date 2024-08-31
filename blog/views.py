from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.

def blog(request):
    blog_pages = BlogPage.objects.all().order_by('order')
    question_page = QuestionPage.objects.first()
      
    context = {
        'blog_pages': blog_pages,
        'question_page': question_page,
    }
    
    return render(request, 'blog/blog.html', context)

def page_details(request, id):
    # جلب الصفحة المحددة أو إظهار خطأ 404 إذا لم يتم العثور عليها
    blog_page = get_object_or_404(BlogPage, id=id)
    
    context = {
        'blog_page': blog_page,
        'sections': blog_page.sections.all().order_by('order'),
    }
    return render(request, 'blog/blog-page.html', context)

def question_page(request):
    question_page = QuestionPage.objects.first() 
    
    context = {
        'question_page': question_page,
        'questions': question_page.questions.all().order_by('order')  # الحصول على الأقسام المرتبطة,
    }
    return render(request, 'blog/question_page.html', context)
