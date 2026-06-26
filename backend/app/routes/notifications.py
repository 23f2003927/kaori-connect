"""Notification routes."""
from flask import Blueprint, request, jsonify, current_app
from ..middleware.auth import require_auth

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/notifications', methods=['GET'])
@require_auth
def get_notifications():
    try:
        result = current_app.supabase.table('notifications') \
            .select('*') \
            .eq('user_id', request.user_id) \
            .order('created_at', desc=True) \
            .limit(30) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@notifications_bp.route('/notifications/<notif_id>/read', methods=['PUT'])
@require_auth
def mark_read(notif_id):
    try:
        current_app.supabase.table('notifications').update({'read': True}).eq('id', notif_id).execute()
        return jsonify({'message': 'Marked as read'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@notifications_bp.route('/notifications/read-all', methods=['PUT'])
@require_auth
def mark_all_read():
    try:
        current_app.supabase.table('notifications').update({'read': True}).eq('user_id', request.user_id).execute()
        return jsonify({'message': 'All notifications marked as read'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
