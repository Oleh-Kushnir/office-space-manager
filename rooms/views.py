from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from .models import Tenant, Lease, UtilityReading, Tariff
from decimal import Decimal, InvalidOperation
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Room, Building, Tenant, Tariff, UtilityReading, UtilityType
from .serializers import (
    RoomSerializer, BuildingSerializer, TenantSerializer,
    LeaseSerializer, UtilityReadingSerializer, TariffSerializer
)

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def submit_reading(request):
    try:
        tenant = request.user.tenant_profile
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Орендаря не знайдено'}, status=404)

    try:
        active_lease = tenant.leases.get(end_date__isnull=True)
    except Lease.DoesNotExist:
        return JsonResponse({'error': 'Активний договір не знайдено'}, status=400)

    current_room = active_lease.room

    utility_type = request.POST.get('utility_type')
    raw_value = request.POST.get('value')

    if not utility_type or not raw_value:
        return JsonResponse({'error': 'Не вказано тип послуги або значення'}, status=400)

    try:
        current_value = Decimal(raw_value)
    except InvalidOperation:
        return JsonResponse({'error': 'Значення повинно бути числом'}, status=400)

    previous_reading = UtilityReading.objects.filter(
        room=current_room,
        utility_type=utility_type
    ).order_by('-reading_date').first()

    previous_value = previous_reading.value if previous_reading else Decimal('0')
    consumed_amount = current_value - previous_value

    if consumed_amount < 0:
        return JsonResponse({'error': 'Новий показник менший за попередній'}, status=400)

    tariff = Tariff.objects.filter(
        utility_type=utility_type,
        effective_from__lte=timezone.now().date()
    ).order_by('-effective_from').first()

    if tariff is None:
        return JsonResponse({'error': 'Активний тариф для цього типу послуги не знайдено'}, status=400)

    total_cost = consumed_amount * tariff.price_per_unit

    new_reading = UtilityReading.objects.create(
        room=current_room,
        utility_type=utility_type,
        value=current_value,
        reading_date=timezone.now().date(),
        consumption=consumed_amount,   # <- те саме consumed_amount, яке порахували вище
        cost=total_cost,                # <- той самий total_cost, яке порахували вище
    )

    return JsonResponse({
        'success': True,
        'message': 'Показник успішно збережено!',
        'consumed': consumed_amount,
        'cost': round(total_cost, 2)
    })


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]


class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]


class UtilityReadingViewSet(viewsets.ModelViewSet):
    queryset = UtilityReading.objects.all()
    serializer_class = UtilityReadingSerializer
    permission_classes = [IsAuthenticated]


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = [IsAuthenticated]