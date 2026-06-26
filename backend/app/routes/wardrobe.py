"""Wardrobe routes."""
from flask import Blueprint, request, jsonify, current_app
from ..middleware.auth import require_auth

wardrobe_bp = Blueprint('wardrobe', __name__)


@wardrobe_bp.route('/wardrobe', methods=['GET'])
@require_auth
def get_items():
    try:
        result = current_app.supabase.table('wardrobe_items') \
            .select('*') \
            .eq('user_id', request.user_id) \
            .order('created_at', desc=True) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe', methods=['POST'])
@require_auth
def add_item():
    data = request.get_json()
    try:
        result = current_app.supabase.table('wardrobe_items').insert({
            'user_id': str(request.user_id),
            'name': data.get('name'),
            'category': data.get('category', 'Tops'),
            'color': data.get('color'),
            'season': data.get('season', 'All Seasons'),
            'occasion': data.get('occasion', 'Casual'),
            'favorite': data.get('favorite', False),
            'image_url': data.get('image_url')
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe/<item_id>', methods=['PUT'])
@require_auth
def update_item(item_id):
    data = request.get_json()
    allowed = ['name', 'category', 'color', 'season', 'occasion', 'favorite', 'image_url']
    updates = {k: v for k, v in data.items() if k in allowed}
    try:
        result = current_app.supabase.table('wardrobe_items').update(updates).eq('id', item_id).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe/<item_id>', methods=['DELETE'])
@require_auth
def delete_item(item_id):
    try:
        current_app.supabase.table('wardrobe_items').delete().eq('id', item_id).eq('user_id', request.user_id).execute()
        return jsonify({'message': 'Item deleted'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe/outfits', methods=['GET'])
@require_auth
def get_outfits():
    try:
        result = current_app.supabase.table('outfits').select('*, outfit_items(*, wardrobe_items(*))').eq('user_id', request.user_id).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe/outfits', methods=['POST'])
@require_auth
def create_outfit():
    data = request.get_json()
    try:
        outfit = current_app.supabase.table('outfits').insert({
            'user_id': str(request.user_id),
            'name': data.get('name', 'My Outfit')
        }).execute()
        
        outfit_id = outfit.data[0]['id']
        for item_id in data.get('items', []):
            current_app.supabase.table('outfit_items').insert({
                'outfit_id': outfit_id,
                'wardrobe_item_id': item_id
            }).execute()
        
        return jsonify(outfit.data), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe/requests', methods=['GET'])
@require_auth
def get_requests():
    try:
        result = current_app.supabase.table('wardrobe_requests') \
            .select('*') \
            .or_(f'from_user_id.eq.{request.user_id},to_user_id.eq.{request.user_id}') \
            .order('created_at', desc=True) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe/requests', methods=['POST'])
@require_auth
def send_request():
    data = request.get_json()
    try:
        result = current_app.supabase.table('wardrobe_requests').insert({
            'from_user_id': str(request.user_id),
            'to_user_id': data.get('to_user_id'),
            'item_id': data.get('item_id'),
            'message': data.get('message', ''),
            'status': 'Pending'
        }).execute()

        # Log activity
        current_app.supabase.table('activity_feed').insert({
            'user_id': str(request.user_id),
            'action': 'wardrobe_request',
            'icon': '👕',
            'text': 'Sent a wardrobe request'
        }).execute()

        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@wardrobe_bp.route('/wardrobe/requests/<req_id>', methods=['PUT'])
@require_auth
def update_request(req_id):
    data = request.get_json()
    status = data.get('status', 'Pending')
    try:
        result = current_app.supabase.table('wardrobe_requests').update({'status': status}).eq('id', req_id).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
