from django.urls import path
from website import views

urlpatterns = [
    # ----------------- Public Pages -----------------
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_page, name='product_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ----------------- Dashboard / CRUD -----------------
    path("dashboard/", views.dashboard, name="dashboard"),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),

    # ----------------- User Management -----------------
    path('users/', views.users_list, name='users_list'),
    path('users/add/', views.add_user, name='add_user'),

    # ----------------- Cart -----------------
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

    # ----------------- API -----------------
    path('api/login/', views.SimpleLoginView.as_view(), name='api_login'),
    path('api/products/<int:id>', views.api_product_list, name='api_product_list'),
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/product/',views.api_product, name='api_admin_prodcut'),
]
