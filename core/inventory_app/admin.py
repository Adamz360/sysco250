from django.contrib import admin
from .models import Product,ProductCategory,Transaction, OrderItem, ReceiverEmail, LowStockNotification, CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Transaction)
admin.site.register(ReceiverEmail)

# added on 24th 2:32am to add role to employee
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'timestamp')



@admin.register(LowStockNotification)
class LowStockNotificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at', 'resolved')
    list_filter = ('resolved',)
    search_fields = ('product__name',)
