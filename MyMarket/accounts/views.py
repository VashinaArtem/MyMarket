# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Product
from .filters import ProductFilter
from .forms import ProductForm

class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context
class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'

# чтобы пользователь мог создать свой продукт
def create_product(request): # функциональные вью, аргумент request-- запрос от пользователя
    form = ProductForm()# создание формы для следующего заполнения

    if request.method == 'POST':# проверка на запрос POST для отправки инфы в бд, method = GET nor POST
        form = ProductForm(request.POST)# загрузка информации в c сайта в form
        if form.is_valid():# проверка на верно введенные данные
            form.save() # .save() -- сохраняет инф в базе данных
            return HttpResponseRedirect('/product/')# после создания товара перенаправление пользователя на главную страницу

    return render(request, 'product_edit.html', {'form': form}) # 1) передает инфу с сайта в HTML при рендеринге
    # 2) то в какой HTML шаблон передать  3) хз


