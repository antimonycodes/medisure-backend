import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medisure.settings')
django.setup()

from django.contrib.auth.models import User
from tracker.models import Manufacturer, Batch, Transaction, UserProfile

def reproduce():
    print("--- Starting Reproduction ---")
    
    # 1. Test Signal
    username = f"test_{uuid.uuid4().hex[:8]}"
    print(f"Creating user: {username}")
    user = User.objects.create_user(username=username, password='password123')
    
    try:
        profile = user.profile
        print(f"Profile created successfully for {username}")
    except UserProfile.RelatedObjectDoesNotExist:
        print(f"ERROR: Profile NOT created for {username}. Signal failed!")
        return

    # 2. Test entities creation (Simulate signup view)
    print("Simulating signup for manufacturer...")
    manufacturer = Manufacturer.objects.create(
        name="Repro Corp",
        wallet_address=f"addr_{username}",
        verified=True
    )
    print(f"Manufacturer created: {manufacturer.id}")
    
    user.profile.role = 'manufacturer'
    user.profile.entity_id = str(manufacturer.id)
    user.profile.save()
    print("Profile updated with manufacturer info")

    # 3. Test Minting (Simulate mint_batch view)
    print("Simulating minting...")
    batch_id = f"BATCH-{uuid.uuid4().hex[:8]}"
    try:
        batch = Batch.objects.create(
            batch_id=batch_id,
            medicine_name="ReproDrug",
            composition="Repro 100mg",
            manufacturer_id=str(manufacturer.id),
            manufactured_date="2024-01-01",
            expiry_date="2026-01-01",
            quantity=1000,
            nft_minted=True,
            qr_code=str(uuid.uuid4())
        )
        print(f"Batch created successfully: {batch.batch_id}")
    except Exception as e:
        print(f"ERROR during batch creation: {e}")
        return

    # 4. Check results
    print(f"Manufacturers count: {Manufacturer.objects.count()}")
    print(f"Batches count: {Batch.objects.count()}")
    
    # 5. Test signin response
    print("Testing signin response...")
    from tracker.auth_views import signin
    from rest_framework.test import APIRequestFactory
    
    factory = APIRequestFactory()
    signin_request = factory.post('/api/auth/signin/', {'username': username, 'password': 'password123'}, format='json')
    signin_response = signin(signin_request)
    print(f"Signin response name: {signin_response.data.get('name')}")
    
    if signin_response.data.get('name') == "Repro Corp":
        print("SUCCESS: Signin response includes correct entity name")
    else:
        print("ERROR: Signin response missing or incorrect name")

    # 6. Test transfer
    print("Simulating transfer...")
    from tracker.views import transfer_batch
    
    # We'll mock verify_wallet_has_asset to return success since we are in a test env without real chain sync
    import tracker.blockfrost_utils as blockfrost_utils
    original_verify = blockfrost_utils.verify_wallet_has_asset
    blockfrost_utils.verify_wallet_has_asset = lambda *args, **kwargs: {'success': True, 'has_asset': True}
    
    transfer_payload = {
        'batch_id': batch.batch_id,
        'from_wallet': 'addr_test_sender',
        'to_wallet': 'addr_test_recipient',
        'tx_hash': 'tx_hash_transfer_123'
    }
    
    # Create request object
    transfer_request = factory.post('/api/transfer/', transfer_payload, format='json')
    transfer_response = transfer_batch(transfer_request)
    
    print(f"Transfer response: {transfer_response.data}")
    
    # Restore original function
    blockfrost_utils.verify_wallet_has_asset = original_verify
    
    # Check if transaction was created
    trans_count = Transaction.objects.filter(batch=batch, transaction_type='TRANSFER').count()
    print(f"Transfer transactions count: {trans_count}")
    
    # Check dashboard status
    dashboard_request = factory.get(f'/api/dashboard/?manufacturer_id={manufacturer.id}')
    from tracker.views import dashboard_stats
    dashboard_response = dashboard_stats(dashboard_request)
    
    batch_in_dashboard = next((b for b in dashboard_response.data['batches'] if b['batch_id'] == batch.batch_id), None)
    print(f"Batch status in dashboard: {batch_in_dashboard['status'] if batch_in_dashboard else 'NOT FOUND'}")
    
    if batch_in_dashboard and batch_in_dashboard['status'] == "In Transit":
        print("SUCCESS: Batch status updated to In Transit")
    else:
        print("ERROR: Batch status failed to update")

    print("--- Reproduction Finished ---")

if __name__ == "__main__":
    reproduce()
