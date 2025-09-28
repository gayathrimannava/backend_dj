from django.contrib import admin
from website.models import Product
from website.models import ProductImage
from website.models import AuthUser, Cart, CartItem
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(AuthUser)
admin.site.register(Cart)
admin.site.register(CartItem)


