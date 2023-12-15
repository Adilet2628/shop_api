from rest_framework import serializers
from django.db.models import Avg
from category.models import Category
from .models import Product

class ProductListSerializers(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('id', 'owner', 'owner_email',
                  'title', 'price', 'image')

    def to_representation(self, instance):
        repr = super(ProductListSerializers, self).to_representation(instance)
        try:
            repr['ratings_avg'] = round(
                instance.ratings.aggregate(Avg('rating'))['rating__avg'],1 )
        except TypeError:
            repr['ratings_avg'] = None
        return repr

class ProductSerializers(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'


    def to_representation(self, instance):
        repr = super(ProductSerializers, self).to_representation(instance)
        try:
            repr['ratings_avg'] = round(
                instance.ratings.aggregate(Avg('rating'))['rating__avg'],1 )
        except TypeError:
            repr['ratings_avg'] = None
        return repr