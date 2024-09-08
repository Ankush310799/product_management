from rest_framework import serializers
from .models import Product, Leads
from django.db.models import Count, Sum
from django.core.exceptions import ValidationError


class LeadSerializer(serializers.ModelSerializer):
    """Serialize lead management instance."""

    class Meta:
        model = Leads
        fields = ["id", "name", "email", "phone_number", "product"]


class ProductSerializer(serializers.ModelSerializer):
    """Serialize product model data"""

    class Meta:
        model = Product
        fields = ["pk", "name", "description", "price"]

    def validate(self, attrs):
        price = attrs.get("price")

        if price < 0:
            raise ValidationError("Please Enter positive value.")
        return super().validate(attrs)


class ProductListSerializer(serializers.ModelSerializer):
    """Serialize product model data"""

    leads_count = serializers.SerializerMethodField("get_enquire_count")

    class Meta:
        model = Product
        fields = ["pk", "name", "description", "price", "leads_count"]

    def validate(self, attrs):
        price = attrs.get("price")

        if price < 0:
            raise ValidationError("Please Enter positive value.")
        return super().validate(attrs)

    def get_enquire_count(
        self,
        obj,
    ):
        """Get count to enquiry count."""
        enq_count = Leads.objects.filter(product=obj.id).aggregate(
            count=Count("product"),
        )
        return enq_count


class LeadReportSerializer(serializers.ModelSerializer):
    """Get lead report"""

    product_count = serializers.SerializerMethodField("get_product_count")
    product = ProductSerializer(Product.objects.all(), many=True)

    class Meta:
        model = Leads
        fields = ["name", "product_count", "product"]

    def get_product_count(self, obj):

        product_count = Leads.objects.filter(id=obj.id).aggregate(
            product_count=Count("product"),
        )
        return product_count
