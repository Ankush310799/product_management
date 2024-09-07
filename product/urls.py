from rest_framework import routers
from .views import ProdcutAPIViews, LeadAPIView, LeadsReportAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import include, path
from rest_framework.permissions import AllowAny

router = routers.DefaultRouter()
router.register(r"product", ProdcutAPIViews, basename="product")


schema_view = get_schema_view(
    openapi.Info(
        title="Product Management API",
        default_version="v1",
        description="product Managemet System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
    path("leads/", LeadAPIView.as_view(), name="lead"),
    path("report/", LeadsReportAPIView.as_view(), name="report"),
]
