from django.db import models


class Rubric(models.Model):
    name = models.CharField('Имя', max_length=200)

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField('Имя', max_length=200)
    picture = models.ImageField(upload_to='market/', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=200, null=True, blank=True)
    market = models.ForeignKey('base.Market', on_delete=models.PROTECT, verbose_name='Магазин')
    rubric = models.ForeignKey('base.Rubric', on_delete=models.PROTECT, verbose_name='Рубрика')
    original_url = models.CharField('url', max_length=500, null=True, blank=True)
    picture = models.ImageField(upload_to='product/', null=True, blank=True)
    vendor_code = models.CharField('Артикул', max_length=16, null=True, blank=True)
    available = models.BooleanField('Отображение товара на сайте', default=False)
    temporary_preparse_available = models.BooleanField('Наличие товара после парсинга', default=False)
    last_update = models.DateTimeField('Дата последней синхронизации', auto_now=False)

    def price(self):
        price = self.prices.order_by('-created').first()
        return price.value if price else None

    def __str__(self):
        return self.name


class Price(models.Model):
    created = models.DateTimeField('Дата цены', auto_now_add=True)
    value = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    product = models.ForeignKey('base.Product', related_name='prices', on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return self.product
