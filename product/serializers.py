from rest_framework import serializers
from .models import Product, Leads
from django.db.models import Count, Sum
from django.core.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    """Serialize product model data"""

    class Meta:
        model = Product
        fields = ["pk", "name", "description", "price"]

    
    def validate(self, attrs):
        price = attrs.get('price')

        if price<0:
            raise ValidationError("Please Enter positive value.")
        return super().validate(attrs)
    

class ProductListSerializer(serializers.ModelSerializer):
    """Serialize product model data"""

    class Meta:
        model = Product
        fields = ["pk", "name", "description", "price","leads"]

    
    def validate(self, attrs):
        price = attrs.get('price')

        if price<0:
            raise ValidationError("Please Enter positive value.")
        return super().validate(attrs)


class LeadSerializer(serializers.ModelSerializer):
    """Serialize lead management instance."""

    # products_count = serializers.SerializerMethodField('get_top_products')
    enquiry_count = serializers.SerializerMethodField('get_enquire_count')

    class Meta:
        model = Leads
        fields = ["id","name", "email", "phone_number", "product", "enquiry_count",]

    # def get_top_products(
    #     self, obj
    # ):
    #     """Get list of top products."""

    #     count = Product.objects.filter(id=obj.product.id).aggregate(
    #         count=Count("interested_prodcut"),
    #     )
    #     return count

    
    def get_enquire_count(self, obj,):

        """ Get count to enquiry count."""
        enq_count = Leads.objects.filter(id=obj).aggregate(
            count=Count("product"),
        )
        return enq_count
    

# class LeadReportSerializer(serializers.Serializer):

#     product = serializers.SerializerMethodField("get_products_count")
#     leads = 

