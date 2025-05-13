from django.db import models

# Create your models here.

class Customer(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last_customer = Customer.objects.order_by('-id').first()
            if last_customer and last_customer.code.startswith("CUST"):
                last_num = int(last_customer.code.replace("CUST", ""))
                self.code = f"CUST{last_num + 1:03d}"
            else:
                self.code = "CUST001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"