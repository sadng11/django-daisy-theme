from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField("نام دسته‌بندی", max_length=150)
    slug = models.SlugField("اسلاگ (شناسه انگلیسی)", unique=True)
    description = models.TextField("توضیحات", blank=True)
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="دسته‌بندی"
    )
    title = models.CharField("عنوان محصول", max_length=200)
    slug = models.SlugField("اسلاگ (شناسه انگلیسی)", unique=True)
    price = models.DecimalField("قیمت (تومان / دلار)", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("موجودی انبار", default=10)
    is_featured = models.BooleanField("محصول ویژه", default=False)
    is_available = models.BooleanField("موجود برای خرید", default=True)
    description = models.TextField("توضیحات محصول", blank=True)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "در انتظار پرداخت"),
        ("processing", "در حال پردازش"),
        ("completed", "تکمیل شده"),
        ("cancelled", "لغو شده"),
    )

    customer_name = models.CharField("نام مشتری", max_length=150)
    customer_email = models.EmailField("ایمیل مشتری")
    status = models.CharField("وضعیت سفارش", max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField("مبلغ کل", max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField("یادداشت سفارش", blank=True)
    created_at = models.DateTimeField("تاریخ ثبت سفارش", auto_now_add=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"سفارش شماره {self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField("تعداد", default=1)
    unit_price = models.DecimalField("قیمت واحد", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "اقلام سفارش"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
