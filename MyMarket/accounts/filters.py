from django_filters import FilterSet,  ModelMultipleChoiceFilter
from .models import Product, Material

# ModelMultipleChoiceFilter -- для вывода сразу всех вариаций одной кнопки(для этой опции нет переменной empty_label)
# ModelChoiceFilter -- для вывода рулетки всех вариаций одной кнопки
class ProductFilter(FilterSet):
    material = ModelMultipleChoiceFilter(
        field_name='productmaterial__material',
        queryset=Material.objects.all(),#cписок всех значений Material
        label='Material',#название кнопки
        #empty_label='all'#вместо ----- пишет all
        conjoined=True,#совмещение материалов
    )
    class Meta:
        model = Product
        fields = {
            # 'productmaterial__material': ['exact'],
            'name': ['icontains'],
            'quantity': ['gt'],
            'price': ['lt',  'gt'],
       }