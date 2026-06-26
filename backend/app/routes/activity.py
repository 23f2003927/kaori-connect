"""Activity feed routes."""
from flask import Blueprint, request, jsonify, current_app
from ..middleware.auth import require_auth

activity_bp = Blueprint('activity', __name__)


@activity_bp.route('/activity', methods=['GET'])
@require_auth
def get_feed():
    page = int(request.args.get('page', 1))
    limit = 20
    offset = (page - 1) * limit
    try:
        result = current_app.supabase.table('activity_feed') \
            .select('*') \
            .order('created_at', desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
