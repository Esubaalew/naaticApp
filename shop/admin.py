from django.contrib import admin

from shop.models import OrderItem, Product, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available_quantity', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'total_price', 'ordered_at', 'status']
    list_filter = ['ordered_at', 'status']
    search_fields = ['product', 'user']
    date_hierarchy = 'ordered_at'


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['order', 'product']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

