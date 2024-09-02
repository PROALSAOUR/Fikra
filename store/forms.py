# from django import forms
# from store.models import Product, ProductVariants

# class ProductVariantsForm(forms.ModelForm):
#     class Meta:
#         model = ProductVariants
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # استخدم id كقيمة اختيارية بدلاً من الاسم
#         self.fields['product'].queryset = Product.objects.all().order_by('pid')
#         self.fields['product'].widget = forms.Select(choices=[(p.id, f'{p.pid} - {p.name}') for p in Product.objects.all()])