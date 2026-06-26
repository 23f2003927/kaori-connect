"""Health planner routes."""
from flask import Blueprint, request, jsonify, current_app
from ..middleware.auth import require_auth

health_bp = Blueprint('health', __name__)


@health_bp.route('/health/plans', methods=['GET'])
@require_auth
def get_plans():
    try:
        result = current_app.supabase.table('health_plans') \
            .select('*') \
            .eq('user_id', request.user_id) \
            .order('created_at', desc=True) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@health_bp.route('/health/plans', methods=['POST'])
@require_auth
def create_plan():
    data = request.get_json()
    try:
        result = current_app.supabase.table('health_plans').insert({
            'user_id': str(request.user_id),
            'type': data.get('type'),
            'target': data.get('target'),
            'status': 'Not Started',
            'streak': 0
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@health_bp.route('/health/plans/<plan_id>', methods=['PUT'])
@require_auth
def update_plan(plan_id):
    data = request.get_json()
    allowed = ['status', 'streak', 'target', 'last_completed']
    updates = {k: v for k, v in data.items() if k in allowed}
    try:
        result = current_app.supabase.table('health_plans').update(updates).eq('id', plan_id).execute()

        # Log activity for status changes
        status = data.get('status')
        if status in ('In Progress', 'Completed'):
            icon = '✅' if status == 'Completed' else '🏃'
            text = f'Completed {data.get("type", "goal")}' if status == 'Completed' else f'Started {data.get("type", "goal")}'
            current_app.supabase.table('activity_feed').insert({
                'user_id': str(request.user_id),
                'action': 'health_update',
                'icon': icon,
                'text': text
            }).execute()

        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@health_bp.route('/health/plans/<plan_id>/log', methods=['POST'])
@require_auth
def log_activity(plan_id):
    data = request.get_json()
    try:
        result = current_app.supabase.table('health_logs').insert({
            'plan_id': plan_id,
            'user_id': str(request.user_id),
            'status': data.get('status', 'In Progress'),
            'notes': data.get('notes')
        }).execute()
        return jsonify(result.data), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@health_bp.route('/health/partner', methods=['GET'])
@require_auth
def get_partner_plans():
    try:
        profile = current_app.supabase.table('profiles').select('partner_id').eq('id', request.user_id).single().execute()
        if not profile.data or not profile.data.get('partner_id'):
            return jsonify([])
        
        result = current_app.supabase.table('health_plans') \
            .select('*') \
            .eq('user_id', profile.data['partner_id']) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@health_bp.route('/health/plans/<plan_id>/react', methods=['POST'])
@require_auth
def react_to_plan(plan_id):
    data = request.get_json()
    reaction = data.get('reaction', '❤️')
    try:
        # Get plan owner to send notification
        plan = current_app.supabase.table('health_plans').select('user_id, type').eq('id', plan_id).single().execute()
        if plan.data:
            current_app.supabase.table('notifications').insert({
                'user_id': plan.data['user_id'],
                'type': 'health_reaction',
                'message': f'Your partner reacted {reaction} to your {plan.data["type"]} goal!'
            }).execute()
        return jsonify({'message': 'Reaction sent!'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@health_bp.route('/health/streaks', methods=['GET'])
@require_auth
def get_streaks():
    try:
        result = current_app.supabase.table('health_plans') \
            .select('type, streak, status') \
            .eq('user_id', request.user_id) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
