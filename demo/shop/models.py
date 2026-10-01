from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=150)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name=_("Category")
    )
    title = models.CharField(_("Product Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    price = models.DecimalField(_("Price (USD)"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Stock Quantity"), default=10)
    is_featured = models.BooleanField(_("Featured Product"), default=False)
    is_available = models.BooleanField(_("Available for Purchase"), default=True)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", _("Pending")),
        ("processing", _("Processing")),
        ("completed", _("Completed")),
        ("cancelled", _("Cancelled")),
    )

    customer_name = models.CharField(_("Customer Name"), max_length=150)
    customer_email = models.EmailField(_("Customer Email"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(_("Total Amount"), max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(_("Order Notes"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{_('Order')} #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    unit_price = models.DecimalField(_("Unit Price"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
