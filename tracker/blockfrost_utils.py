from blockfrost import BlockFrostApi, ApiError
from django.conf import settings

def get_blockfrost_api():
    """Initialize and return Blockfrost API instance"""
    return BlockFrostApi(
        project_id=settings.BLOCKFROST_PROJECT_ID,
        base_url=f"https://cardano-{settings.BLOCKFROST_NETWORK}.blockfrost.io/api"
    )

def get_transaction_utxos(tx_hash):
    """Get UTXOs for a transaction"""
    try:
        api = get_blockfrost_api()
        return {
            'success': True,
            'data': api.transaction_utxos(tx_hash)
        }
    except ApiError as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_address_info(address):
    """Get information for an address"""
    try:
        api = get_blockfrost_api()
        return {
            'success': True,
            'data': api.address(address)
        }
    except ApiError as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_asset_info(policy_id, asset_name):
    """Get asset information from Blockfrost"""
    try:
        api = get_blockfrost_api()
        asset_id = f"{policy_id}{asset_name}"
        asset = api.asset(asset_id)
        return {
            'success': True,
            'data': asset
        }
    except ApiError as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_asset_history(policy_id, asset_name):
    """Get transaction history for an asset"""
    try:
        api = get_blockfrost_api()
        asset_id = f"{policy_id}{asset_name}"
        history = api.asset_history(asset_id)
        return {
            'success': True,
            'data': history
        }
    except ApiError as e:
        return {
            'success': False,
            'error': str(e)
        }

def verify_wallet_has_asset(wallet_address, policy_id, asset_name):
    """Verify if a wallet holds a specific asset"""
    import time
    for attempt in range(3):
        try:
            api = get_blockfrost_api()
            asset_id = f"{policy_id}{asset_name}"
            addresses = api.asset_addresses(asset_id)
            print(f"DEBUG (Attempt {attempt+1}): Found {len(addresses) if isinstance(addresses, list) else 1} holders for {asset_id}")
            
            if not isinstance(addresses, list):
                if hasattr(addresses, 'address'):
                    addresses = [addresses]
                else:
                    addresses = []
            
            for addr in addresses:
                print(f"DEBUG: Holder: {addr.address}")
                if addr.address == wallet_address:
                    return {
                        'success': True,
                        'has_asset': True,
                        'quantity': getattr(addr, 'quantity', '1')
                    }
            
            if attempt < 2:
                print("DEBUG: Asset not yet found in recipient wallet. Retrying in 10s...")
                time.sleep(10)
                
        except ApiError as e:
            if attempt < 2:
                time.sleep(10)
                continue
            return {
                'success': False,
                'error': str(e)
            }
    
    return {
        'success': True,
        'has_asset': False
    }