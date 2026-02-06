from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Manufacturer, Distributor, Pharmacy, Batch, Transaction, PharmacyInventory, Cart, CartItem, Order, OrderItem, UserProfile
from .serializers import (
    ManufacturerSerializer, 
    DistributorSerializer, 
    PharmacySerializer, 
    BatchSerializer, 
    TransactionSerializer,
    PharmacyInventorySerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer
)
import requests
import uuid

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class DistributorViewSet(viewsets.ModelViewSet):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer

class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class PharmacyInventoryViewSet(viewsets.ModelViewSet):
    queryset = PharmacyInventory.objects.all()
    serializer_class = PharmacyInventorySerializer

@api_view(['POST'])
def mint_batch(request):
    try:
        batch_data = request.data
        qr_code = str(uuid.uuid4())
        
        batch = Batch.objects.create(
            batch_id=batch_data['batch_id'],
            medicine_name=batch_data['medicine_name'],
            composition=batch_data['composition'],
            manufacturer_id=batch_data['manufacturer_id'],
            manufactured_date=batch_data['manufactured_date'],
            expiry_date=batch_data['expiry_date'],
            quantity=batch_data['quantity'],
            policy_id=batch_data.get('policy_id'),
            asset_name=batch_data.get('asset_name'),
            nft_minted=True,
            qr_code=qr_code
        )
        
        Transaction.objects.create(
            batch=batch,
            transaction_type='MINT',
            to_wallet=batch_data['manufacturer_wallet'],
            tx_hash=batch_data['tx_hash']
        )
        
        return Response({
            'success': True,
            'batch_id': str(batch.id),
            'qr_code': qr_code,
            'message': 'Batch minted successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_medicine(request, qr_code):
    try:
        from .blockfrost_utils import get_asset_info
        
        batch = Batch.objects.get(qr_code=qr_code)
        
        blockchain_data = None
        if batch.policy_id and batch.asset_name:
            result = get_asset_info(batch.policy_id, batch.asset_name)
            if result['success']:
                blockchain_data = result['data']
        
        return Response({
            'success': True,
            'medicine_name': batch.medicine_name,
            'batch_id': batch.batch_id,
            'manufacturer': batch.manufacturer.name,
            'manufactured_date': batch.manufactured_date,
            'expiry_date': batch.expiry_date,
            'composition': batch.composition,
            'verified': batch.nft_minted,
            'policy_id': batch.policy_id,
            'asset_name': batch.asset_name,
            'blockchain_proof': blockchain_data
        }, status=status.HTTP_200_OK)
        
    except Batch.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Invalid QR code'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def track_journey(request, batch_id):
    try:
        batch = Batch.objects.get(batch_id=batch_id)
        transactions = Transaction.objects.filter(batch=batch).order_by('timestamp')
        
        journey = []
        for tx in transactions:
            journey.append({
                'type': tx.transaction_type,
                'from': tx.from_wallet,
                'to': tx.to_wallet,
                'timestamp': tx.timestamp,
                'tx_hash': tx.tx_hash
            })
        
        return Response({
            'success': True,
            'batch_id': batch_id,
            'medicine_name': batch.medicine_name,
            'journey': journey
        }, status=status.HTTP_200_OK)
        
    except Batch.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Batch not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def transfer_batch(request):
    try:
        from .blockfrost_utils import verify_wallet_has_asset
        
        transfer_data = request.data
        batch = Batch.objects.get(batch_id=transfer_data['batch_id'])
        
        if batch.policy_id and batch.asset_name:
            verification = verify_wallet_has_asset(
                transfer_data['to_wallet'],
                batch.policy_id,
                batch.asset_name
            )
            
            if not verification.get('success') or not verification.get('has_asset'):
                return Response({
                    'success': False,
                    'error': 'Asset not found in receiving wallet'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        Transaction.objects.create(
            batch=batch,
            transaction_type='TRANSFER',
            from_wallet=transfer_data['from_wallet'],
            to_wallet=transfer_data['to_wallet'],
            tx_hash=transfer_data['tx_hash']
        )
        
        return Response({
            'success': True,
            'message': 'Transfer recorded successfully',
            'batch_id': batch.batch_id
        }, status=status.HTTP_201_CREATED)
        
    except Batch.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Batch not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard_stats(request):
    try:
        manufacturer_id = request.query_params.get('manufacturer_id')
        
        if not manufacturer_id:
            return Response({'error': 'manufacturer_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_batches = Batch.objects.filter(manufacturer_id=manufacturer_id).count()
        minted = Batch.objects.filter(manufacturer_id=manufacturer_id, nft_minted=True).count()
        
        manufacturer_batches = Batch.objects.filter(manufacturer_id=manufacturer_id)
        in_transit = Transaction.objects.filter(
            batch__in=manufacturer_batches, 
            transaction_type='TRANSFER'
        ).values('batch').distinct().count()
        
        batch_list = []
        
        for batch in manufacturer_batches:
            if batch.nft_minted:
                transfers = Transaction.objects.filter(batch=batch, transaction_type='TRANSFER').count()
                status_text = "In Transit" if transfers > 0 else "Minted"
            else:
                status_text = "Pending"
            
            batch_list.append({
                'batch_id': batch.batch_id,
                'medicine_name': batch.medicine_name,
                'composition': batch.composition,
                'expiry_date': batch.expiry_date,
                'status': status_text
            })
        
        return Response({
            'success': True,
            'total_batches': total_batches,
            'minted': minted,
            'in_transit': in_transit,
            'batches': batch_list
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pharmacy_inventory(request, pharmacy_id):
    try:
        inventory = PharmacyInventory.objects.filter(pharmacy_id=pharmacy_id, in_stock=True)
        serializer = PharmacyInventorySerializer(inventory, many=True)
        
        return Response({
            'success': True,
            'inventory': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_cart(request):
    try:
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        serializer = CartSerializer(cart)
        
        return Response({
            'success': True,
            'cart': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_to_cart(request):
    try:
        user_id = request.data.get('user_id')
        inventory_id = request.data.get('inventory_id')
        quantity = request.data.get('quantity', 1)
        
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        inventory_item = PharmacyInventory.objects.get(id=inventory_id)
        
        if quantity > inventory_item.quantity_available:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            inventory_item=inventory_item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({
            'success': True,
            'message': 'Item added to cart'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        
        return Response({
            'success': True,
            'message': 'Item removed from cart'
        }, status=status.HTTP_200_OK)
        
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        quantity = request.data.get('quantity')
        
        if quantity > cart_item.inventory_item.quantity_available:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            'success': True,
            'message': 'Cart updated'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def clear_cart(request):
    try:
        user_id = request.query_params.get('user_id')
        cart = Cart.objects.get(user_id=user_id)
        cart.items.all().delete()
        
        return Response({
            'success': True,
            'message': 'Cart cleared'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_order(request):
    try:
        user_id = request.data.get('user_id')
        pharmacy_id = request.data.get('pharmacy_id')
        
        cart = Cart.objects.get(user_id=user_id)
        
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            user_id=user_id,
            pharmacy_id=pharmacy_id,
            total_amount=cart.total_price
        )
        
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                inventory_item=cart_item.inventory_item,
                quantity=cart_item.quantity,
                price_per_unit=cart_item.inventory_item.price_per_unit,
                subtotal=cart_item.subtotal
            )
            
            inventory = cart_item.inventory_item
            inventory.quantity_available -= cart_item.quantity
            if inventory.quantity_available <= 0:
                inventory.in_stock = False
            inventory.save()
        
        cart.items.all().delete()
        
        return Response({
            'success': True,
            'order_id': str(order.id),
            'message': 'Order created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        
        return Response({
            'success': True,
            'order': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_orders(request):
    try:
        user_id = request.query_params.get('user_id')
        orders = Order.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        
        return Response({
            'success': True,
            'orders': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.data.get('status')
        
        order.status = new_status
        order.save()
        
        return Response({
            'success': True,
            'message': 'Order status updated'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.profile.role,
                'date_joined': user.date_joined
            }
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_users_by_role(request):
    try:
        role = request.query_params.get('role')
        
        if role:
            profiles = UserProfile.objects.filter(role=role)
            users = [profile.user for profile in profiles]
        else:
            users = User.objects.all()
        
        user_list = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.profile.role,
            'date_joined': user.date_joined
        } for user in users]
        
        return Response({
            'success': True,
            'users': user_list
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)