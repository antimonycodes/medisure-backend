from blockfrost import BlockFrostApi, ApiError
from django.conf import settings

def get_blockfrost_api():
    """Initialize and return Blockfrost API instance"""
    return BlockFrostApi(
        project_id=settings.BLOCKFROST_PROJECT_ID,
        base_url=f"https://cardano-{settings.BLOCKFROST_NETWORK}.blockfrost.io/api"
    )

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
    try:
        api = get_blockfrost_api()
        asset_id = f"{policy_id}{asset_name}"
        addresses = api.asset_addresses(asset_id)
        
        for addr in addresses:
            if addr.address == wallet_address:
                return {
                    'success': True,
                    'has_asset': True,
                    'quantity': addr.quantity
                }
        
        return {
            'success': True,
            'has_asset': False
        }
    except ApiError as e:
        return {
            'success': False,
            'error': str(e)
        }