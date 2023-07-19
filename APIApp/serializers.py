from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    def validate(self, attrs):
        if attrs['price'] <= 0:
            raise serializers.ValidationError("Price has to be greater than 0")

        if len(attrs['name']) > 255 or len(attrs['name']) < 3:
            raise serializers.ValidationError("Name has to be between 3 and 255 characters")

        if len(attrs['description']) < 10:
            raise serializers.ValidationError("Description has to be greater than 10 characters")

        return attrs

    class Meta:
        model = Product
        fields = '__all__'
