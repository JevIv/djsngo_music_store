from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class MediaType(models.Model):

    name = models.CharField(max_length=100, verbose_name='Type of media')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'


class Member(models.Model):
    """Musician"""

    name = models.CharField(max_length=255, verbose_name='Name of musician')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Musician'
        verbose_name_plural = 'Musicians'


class Genre(models.Model):
    """Musical genre"""

    name = models.CharField(max_length=50, verbose_name='Name of genre')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Artist(models.Model):
    """Artist"""

    name = models.CharField(max_length=255, verbose_name='Artist name/group')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, verbose_name='Band member', related_name='artist')
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name} | {self.genre.name}"

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'


class Album(models.Model):
    """Album"""

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Artist')
    name = models.CharField(max_length=255, verbose_name='Album name')
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE, verbose_name='Media')
    songs_list = models.CharField(verbose_name='Track list')
    release_date = models.DateField(verbose_name='Release date')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.CharField(verbose_name='Description', default='Description is coming soon')
    stock = models.IntegerField(default=1, verbose_name='Available in stock')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    offer_of_the_week = models.BooleanField(default=False, verbose_name='Offer of the week?')
    slug = models.SlugField()

    def __str__(self):
        return f"{self.id} | {self.artist.name} | {self.name}"

    @property
    def ct_model(self):
        return self._meta.model.name

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


class CartProduct(models.Model):
    """Cart product"""
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField(id)
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveBigIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')

    def __str__(self):
        return f"Product: {self.content_object.name} (for cart)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_type.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cart product'
        verbose_name_plural = 'Cart products'


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    product = models.ManyToManyField(
        CartProduct, blank=True, null=True, related_name='related_cart', verbose_name='Cart products')
    total_products = models.IntegerField(default=0, verbose_name='Total products quantity')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return (self.id)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'