from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "stock",
        "is_featured",
        "is_available",
        "created_at",
    )
    list_filter = ("category", "is_featured", "is_available", "created_at")
    search_fields = ("title", "description", "slug")
    list_editable = ("price", "stock", "is_available")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (
            None,
            {
                "fields": ("category", "title", "slug"),
            },
        ),
        (
            "Pricing & Inventory",
            {
                "fields": (("price", "stock"), ("is_featured", "is_available")),
            },
        ),
        (
            "Details",
            {
                "classes": ("collapse",),
                "fields": ("description",),
            },
        ),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_email",
        "status",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_email", "notes")
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"
