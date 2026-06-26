"""Selfie routes."""
from flask import Blueprint, request, jsonify, current_app
from ..middleware.auth import require_auth
import random

selfies_bp = Blueprint('selfies', __name__)


@selfies_bp.route('/selfies', methods=['GET'])
@require_auth
def get_selfies():
    page = int(request.args.get('page', 1))
    limit = 20
    offset = (page - 1) * limit
    try:
        result = current_app.supabase.table('selfies') \
            .select('*') \
            .order('created_at', desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@selfies_bp.route('/selfies/random', methods=['GET'])
@require_auth
def get_random_selfie():
    try:
        result = current_app.supabase.table('selfies').select('*').execute()
        if result.data:
            selfie = random.choice(result.data)
            return jsonify(selfie)
        return jsonify({'message': 'No selfies found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@selfies_bp.route('/selfies/<selfie_id>/react', methods=['POST'])
@require_auth
def react_to_selfie(selfie_id):
    data = request.get_json()
    try:
        current_app.supabase.table('selfie_reactions').upsert({
            'selfie_id': selfie_id,
            'user_id': str(request.user_id),
            'reaction': data.get('reaction', '❤️')
        }).execute()
        return jsonify({'message': 'Reaction saved!'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@selfies_bp.route('/selfies/<selfie_id>', methods=['DELETE'])
@require_auth
def delete_selfie(selfie_id):
    try:
        current_app.supabase.table('selfies').delete().eq('id', selfie_id).eq('user_id', request.user_id).execute()
        return jsonify({'message': 'Selfie deleted'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
