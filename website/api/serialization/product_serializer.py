from rest_framework import serializers
from website.models import Product   # import from the right location

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [ 'name', 'price', 'description']
