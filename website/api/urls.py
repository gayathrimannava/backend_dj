# website/api/urls.py
from django.urls import path
from website.api.views import ProductListCreateView, ProductRetrieveUpdateDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ---------------- JWT Authentication ----------------
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # get access + refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # refresh token

    # ---------------- Products ----------------
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),          # GET: list, POST: add
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product_detail'),  # GET/PUT/DELETE single product
    path('ping',ProductRetrieveUpdateDeleteView.as_view(),name="ping"),
]
