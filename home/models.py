from django.db import models
from django.utils.timezone import now
import random

# Create your models here.
"""


3. Historical Performance Model
This model optionally stores historical data on vendor performance, enabling trend analysis.
● Fields:
● vendor: ForeignKey - Link to the Vendor model.
● date: DateTimeField - Date of the performance record.
● on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
● quality_rating_avg: FloatField - Historical record of the quality rating average.
● average_response_time: FloatField - Historical record of the average response
time.
● fulfillment_rate: FloatField - Historical record of the fulfilment rate.
These models form the backbone of the Vendor Management System, enabling
comprehensive tracking and analysis of vendor performance over time. The performance
metrics are updated based on interactions recorded in the Purchase Order model

Metrics:
● On-Time Delivery Rate: Percentage of orders delivered by the promised date.
● Quality Rating: Average of quality ratings given to a vendor’s purchase orders.
● Response Time: Average time taken by a vendor to acknowledge or respond to
purchase orders.
● Fulfilment Rate: Percentage of purchase orders fulfilled without issues.
● Model Design: Add fields to the vendor model to store these performance metrics.
"""

choice_status = (
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("canceled", "Canceled")
)


class Vendor(models.Model):
    name = models.CharField(max_length=130)
    contact_details = models.CharField(max_length=13)
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.vendor_code = random.randint(10000, 99999)

        super(Vendor, self).save(*args, **kwargs)
        return self
    
    def __str__(self):
        return self.name



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=10, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date =  models.DateTimeField(default=now)
    delivery_date = models.DateTimeField(default=now)
    delivery_complete_date = models.DateTimeField(default=now)
    items = models.JSONField(default=dict, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    status = models.CharField(choices=choice_status, max_length=10, default="pending")
    quality_rating = models.FloatField(default=0)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.po_number = random.randint(10000, 99999)
        super(PurchaseOrder, self).save(*args, **kwargs)
        return self
    
    def __str__(self):
        return self.po_number
    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    performance_date = models.DateField(default=now)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    class Meta:
        unique_together = ("vendor", "performance_date")
