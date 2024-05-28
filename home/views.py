from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    Vendor, VendorSerializer,
    PurchaseOrder, PurchaseOrderSerializer,
    HistoricalPerformance, HistoricalSerializer
)
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import *
# Create your views here.

# def performance_vendor_report_update(vendor):
#     today = datetime.today()
#     performance = HistoricalPerformance.objects.filter(vendor=vendor, performance_date=today)
#     if performance:
#         obj = performance[0]
#     else:
#         obj = HistoricalPerformance(vendor=vendor, performance_date=today)
#     """
#     delivery_date,
#     delivery_complete_date
#     """

#     order = PurchaseOrder.objects.filter(vendor=vendor, order_date=today).aggregate(
#         total_order=Count('id'), 
#         total_on_time_order = Count('id', filter=Q(delivery_date__gte=F('delivery_complete_date'))),
#         on_time_rate_avg = (F('total_on_time_order')/F('total_order'))*100,
#         rating_avg = Avg('quality_rating')
#     )

#     print(order)

#     obj.on_time_delivery_rate = order['on_time_rate_avg'] if order['on_time_rate_avg'] is not None else 0

    

#     obj.save()

def performance_vendor_report_update(vendor):

    order = PurchaseOrder.objects.filter(vendor=vendor).aggregate(
        total_order=Count('id'), 
        total_on_time_order = Count('id', filter=Q(delivery_date__gte=F('delivery_complete_date'))),
        quality_rating_avg = Avg('quality_rating'),
        fulfillment = Count('id', filter=Q(issue_date=None))
    )
    
    print(order)
    vendor.quality_rating_avg = order['quality_rating_avg']

    if order['total_on_time_order']:
        vendor.on_time_delivery_rate = (order['total_on_time_order'] / order['total_order'])*100

    if order['fulfillment']:
        vendor.fulfillment_rate = (order['fulfillment'] / order['total_order'])*100

    
    """
    on_time_delivery_rate = models.FloatField(default=0)..
    quality_rating_avg = models.FloatField(default=0)..
    average_response_time = models.FloatField(default=0)
    fulfillment_rate
    """


    vendor.save()


class VendorViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    models = Vendor
    serializer_class = VendorSerializer
    queryset = models.objects.all()

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        performance_vendor_report_update(vendor=vendor)
        queryset = HistoricalPerformance.objects.filter(vendor=vendor)
        data = {
            "vendor":self.serializer_class(vendor).data,
            "performance":HistoricalSerializer(queryset, many=True).data
        }
        
        
        return Response(data)

class PurchaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    models = PurchaseOrder
    serializer_class = PurchaseOrderSerializer
    queryset = models.objects.all()

    
        
    