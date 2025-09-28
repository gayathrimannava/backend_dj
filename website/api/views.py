from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from website.models import Product
from website.api.serialization.product_serializer import ProductSerializer
import logging


class ProductListCreateView(APIView):
    # Temporarily removed authentication requirement for testing
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        logger = logging.getLogger(__name__) 
        logger.error("This is an informational message.")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # ---------- FIXED ----------
    
    def post(self, request):
        logger = logging.getLogger(__name__) 
        logger.info("This is an informational message.")
        serializer = ProductSerializer(data=request.data)
        try:
            if serializer.is_valid():
                product = serializer.save()                      # ❶ really writes to DB
                print(f"Product saved → ID {product.id}")        # ❷ see this in the terminal
                return Response(                                 # ❸ return ONLY the new product
                    ProductSerializer(product).data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

        
    

class ProductRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"detail": "Not found."}, status=404)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
@method_decorator(csrf_exempt, name='dispatch')  # Fallback exemption
class ProductRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_400_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Optional: CSRF token view (not needed anymore, but kept if useful)
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrftoken': token})
