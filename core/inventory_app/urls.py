# urls.py
from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', CustomLoginView.as_view(template_name='inventory_page/login_page.html'), name='login'),
    path('products/', views.product_list, name='product_list'),
    path('category/', views.category_list, name='category_list'),
    path('category/<int:category_id>/delete', views.delete_category, name='delete_category'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/create/', views.create_product, name='create_product'),
    path('category/create/', views.create_category, name='create_category'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/update/', views.update_product, name='update_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:product_id>/transaction/', views.transaction_create, name='transaction_create'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('employees/', views.employee_list, name='employee_list'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('delete_admin/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('sales/', views.sales_page, name='sales_page'),
    path('add-email/', views.add_email, name='add_email'),
    path('email-list/', views.email_list, name='email_list'),
    path('delete-email/<int:email_id>/delete/', views.delete_email, name='delete_email'),
    path('products-by-category/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('login/', CustomLoginView.as_view(template_name='inventory_page/login_page.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('invoice-print/', views.invoice_print, name='invoice_print'),
    path('product-quantity/<int:product_id>/', views.get_product_quantity, name='product_quantity'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('notification/', views.notification_view, name='notification'),
    path('revenue-year/', views.total_revenue_annual, name='total_revenue_year'),
    path('revenue-day/', views.total_revenue_day, name='total_revenue_day'),
    path('revenue-week/', views.total_revenue_week, name='total_revenue_week'),
    path('revenue-month/', views.total_revenue_month, name='total_revenue_month'),
]


