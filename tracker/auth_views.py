from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from tracker.models import Manufacturer, Pharmacy, Distributor

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        role = request.data.get('role', 'patient')
        wallet_address = request.data.get('wallet_address', '')
        name = request.data.get('name', username)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.profile.role = role
        
        entity_id = None
        if role == 'manufacturer':
            entity = Manufacturer.objects.create(
                name=name,
                wallet_address=wallet_address or f"wallet_{username}",
                verified=False
            )
            entity_id = str(entity.id)
        elif role == 'pharmacy':
            entity = Pharmacy.objects.create(
                name=name,
                wallet_address=wallet_address or f"wallet_{username}",
                verified=False
            )
            entity_id = str(entity.id)
        elif role == 'distributor':
            entity = Distributor.objects.create(
                name=name,
                wallet_address=wallet_address or f"wallet_{username}",
                verified=False
            )
            entity_id = str(entity.id)
        
        user.profile.entity_id = entity_id
        user.profile.save()
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'role': role,
            'entity_id': entity_id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    try:
        identifier = (request.data.get('username') or '').strip()
        password = request.data.get('password') or ''

        if not identifier or not password:
            return Response(
                {'error': 'Username/email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1) Direct username auth
        user = authenticate(username=identifier, password=password)

        # 2) Case-insensitive username fallback
        if not user:
            try:
                matched_user = User.objects.get(username__iexact=identifier)
                user = authenticate(username=matched_user.username, password=password)
            except User.DoesNotExist:
                pass

        # 3) Email login fallback
        if not user:
            try:
                matched_user = User.objects.get(email__iexact=identifier)
                user = authenticate(username=matched_user.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            role = user.profile.role
            entity_id = user.profile.entity_id
            
            return Response({
                'success': True,
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'role': role,
                'entity_id': entity_id
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
