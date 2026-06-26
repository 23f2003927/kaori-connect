"""Profile and partner linking routes."""
from flask import Blueprint, request, jsonify, current_app
from ..middleware.auth import require_auth

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get current user's profile."""
    try:
        result = current_app.supabase.table('profiles').select('*').eq('id', request.user_id).single().execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@profile_bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update current user's profile."""
    data = request.get_json()
    allowed_fields = ['display_name', 'avatar_url']
    updates = {k: v for k, v in data.items() if k in allowed_fields}
    
    try:
        result = current_app.supabase.table('profiles').update(updates).eq('id', request.user_id).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@profile_bp.route('/profile/partner', methods=['GET'])
@require_auth
def get_partner():
    """Get partner's profile."""
    try:
        profile = current_app.supabase.table('profiles').select('partner_id').eq('id', request.user_id).single().execute()
        if not profile.data or not profile.data.get('partner_id'):
            return jsonify({'message': 'No partner linked'}), 404
        
        partner = current_app.supabase.table('profiles').select('id, display_name, avatar_url').eq('id', profile.data['partner_id']).single().execute()
        return jsonify(partner.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@profile_bp.route('/partner/link', methods=['POST'])
@require_auth
def link_partner():
    """Link with a partner using their code."""
    data = request.get_json()
    code = data.get('code', '').strip().upper()
    
    if not code:
        return jsonify({'message': 'Partner code is required'}), 400
    
    try:
        # Find partner by code
        partner = current_app.supabase.table('profiles').select('id, display_name').eq('partner_code', code).single().execute()
        if not partner.data:
            return jsonify({'message': 'Partner code not found'}), 404
        
        if partner.data['id'] == str(request.user_id):
            return jsonify({'message': "You can't link with yourself"}), 400
        
        partner_id = partner.data['id']
        
        # Create couple record
        current_app.supabase.table('couples').insert({
            'user1_id': str(request.user_id),
            'user2_id': partner_id
        }).execute()
        
        # Update both profiles
        current_app.supabase.table('profiles').update({'partner_id': partner_id}).eq('id', request.user_id).execute()
        current_app.supabase.table('profiles').update({'partner_id': str(request.user_id)}).eq('id', partner_id).execute()
        
        return jsonify({'message': f'Linked with {partner.data["display_name"]}!', 'partner': partner.data})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
