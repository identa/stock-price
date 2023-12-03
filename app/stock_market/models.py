from django.db import models
import uuid


# Create your models here.
class StockModel(models.Model):
    class Meta:
        db_table = "stock"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock_symbol = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class StockPriceModel(models.Model):
    class Meta:
        db_table = "stock_price"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stock = models.ForeignKey(StockModel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "symbol": self.stock.stock_symbol,
            "price": self.price,
            "quantity": self.quantity,
        }
