from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from product.serializers import (
    ProductSerializer,
    LeadSerializer,
    ProductListSerializer,
    LeadReportSerializer
)
from .models import Product, Leads
from rest_framework import status
from django.db.models import Q, Count
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProdcutAPIViews(viewsets.ModelViewSet):
    """Product API views"""

    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return ProductSerializer
        else:
            return ProductListSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadAPIView(ListCreateAPIView):
    """Lead API views"""

    queryset = Leads.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class LeadsReportAPIView(APIView):
    """List of Leads"""

    serializer_class = ProductListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        AllowAny,
    ]

    def get(self, request, *args, **kwargs):
        """
        Return a list of leads on the given urls.
        """
        queryset = []

        start_date = self.request.query_params.get("start_date") or ""
        end_date = self.request.query_params.get("end_date") or ""
        top_products = self.request.query_params.get("top_products") or ""
        last_products = self.request.query_params.get("last_products") or ""

        # Return leads between timespan
        if start_date and end_date:
            """Get leads report between given time span."""

            queryset = Leads.objects.filter(
                Q(created_at__gte=start_date) and Q(created_at__lte=end_date)
            )
            serialize_data = LeadSerializer(queryset, many=True)
            result = serialize_data.data
            return Response(result, status=status.HTTP_200_OK)

        elif top_products:
            """ Get list of top 10 prodcuts with highest leads"""

            queryset = Product.objects.annotate(
                lead_count=Count("interested_products")
            ).order_by("-lead_count")[:10]
            serialize_data = ProductListSerializer(queryset, many=True)
            result = serialize_data.data
            return Response(result, status=status.HTTP_200_OK)

        elif last_products:
            """Get list of last 10 products with lowest leads."""

            queryset = Product.objects.annotate(
                lead_count=Count("interested_products")
            ).order_by("lead_count")[:10]

            serialize_data = ProductListSerializer(queryset, many=True)
            result = serialize_data.data
            return Response(result, status=status.HTTP_200_OK)

        else:
            # Return list of Number of products for each Lead.
            queryset = Leads.objects.all()
            if queryset:
                serialize_data = LeadReportSerializer(queryset, many=True)
                result = serialize_data.data
                return Response(result, status=status.HTTP_200_OK)
            
            return Response({"error":"No data found"}, status=status.HTTP_204_NO_CONTENT)
