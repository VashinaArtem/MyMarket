from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime, timezone
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products')
    price = models.PositiveIntegerField(default=0)
    material = models.ManyToManyField('Material', through='ProductMaterial')
    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'


class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    # здесь показываем, что с таблицей Product идет связь ManyToMany через ProductOrder
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        #???
        self.save()

    def get_duration(self):
        #если заказ выполнен, то отправляем все время выполнения заказа
        if self.complete:
            return (self.time_out - self.time_in).total_seconds()//60
        else:
            return (datetime.now(timezone.utc) - self.time_in).total_seconds()//60

# тут идет соответствие номера заказа с номером продукта
# (плюс количество каждого из продуктов в каждом хаказе)
# одинаковые продукты могут быть в разных заказах
# и в одном заказе могут содержаться разные продукты
class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    # self - ProductOrder
    def product_sum(self):
        # тут мы обращаемся к self->product->price
        product_price = self.product.price
        # возвращаем цену, исходя из количества
        return product_price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()





class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        last_name = self.full_name.split()[0]
        return last_name



