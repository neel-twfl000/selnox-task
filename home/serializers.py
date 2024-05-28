from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        
    
        extra_kwargs = {
            'vendor_code': {'read_only': True},
            'on_time_delivery_rate': {'read_only': True},
            'quality_rating_avg': {'read_only': True},
            'fulfillment_rate': {'read_only': True},
            'average_response_time': {'read_only': True},
        }

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

        extra_kwargs = {
            'po_number': {'read_only': True},
        }

class HistoricalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
