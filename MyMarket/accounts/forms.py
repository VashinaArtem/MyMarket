from django import forms
from .models import Product

# форма для заполнения
class ProductForm(forms.ModelForm):
   class Meta:
       model = Product
       fields = [
           'name',
           'description',
           'category',
           'price',
           'quantity',
       ]



# альтернотивная запись. В ней тот же функционал, но без использывания Meta-класса
# class ProductForm(forms.Form):
#     name = forms.CharField(label='Name')
#     description = forms.CharField(label='Description')
#     quantity = forms.IntegerField(label='Quantity')
#     category = forms.ModelChoiceField(
#         label='Category', queryset=Category.objects.all(),
#     )
#     price = forms.FloatField(label='Price')