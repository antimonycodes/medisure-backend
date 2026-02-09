from rest_framework import serializers
from .models import Manufacturer, Distributor, Pharmacy, Batch, Transaction, PharmacyInventory, Cart, CartItem, Order, OrderItem

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = '__all__'

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'

class BatchSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)
    
    class Meta:
        model = Batch
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    batch_id = serializers.CharField(source='batch.batch_id', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'

class PharmacyInventorySerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.CharField(source='pharmacy.name', read_only=True)
    medicine_name = serializers.CharField(source='batch.medicine_name', read_only=True)
    batch_id = serializers.CharField(source='batch.batch_id', read_only=True)
    
    batch_details = BatchSerializer(source='batch', read_only=True)
    
    class Meta:
        model = PharmacyInventory
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='inventory_item.batch.medicine_name', read_only=True)
    price_per_unit = serializers.DecimalField(source='inventory_item.price_per_unit', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    pharmacy_name = serializers.CharField(source='inventory_item.pharmacy.name', read_only=True)
    pharmacy_id = serializers.UUIDField(source='inventory_item.pharmacy.id', read_only=True)
    
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='inventory_item.batch.medicine_name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    pharmacy_name = serializers.CharField(source='pharmacy.name', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'