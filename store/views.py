from django.shortcuts import render
from store.models import AdsSlider, Brand
# Create your views here.

def index(request):
    
    ads = AdsSlider.objects.filter(show=True)
    brands = Brand.objects.filter(featured=True).only('title', 'img')
    
    context = {
        'ads': ads,
        'brands':brands,
    }
    
    return render(request, 'store/index.html', context)