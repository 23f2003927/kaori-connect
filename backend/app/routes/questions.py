"""Questions routes."""
from flask import Blueprint, request, jsonify, current_app
from ..middleware.auth import require_auth
import random

questions_bp = Blueprint('questions', __name__)

# Built-in question bank
QUESTION_BANK = {
    'Funny': [
        "What's the most embarrassing thing you've ever done on a date?",
        "If we were in a zombie apocalypse, what's your survival plan for us?",
        "What animal do you think I'd be and why?",
        "If we switched bodies for a day, what would you do first?",
    ],
    'Deep': [
        "What's one thing about me that always makes you smile?",
        "What does 'home' feel like to you?",
        "What moment made you realize you loved me?",
        "If you could relive one day of our relationship, which would it be?",
    ],
    'Romantic': [
        "What's your favorite memory of us together?",
        "What made you fall in love with me?",
        "What song reminds you of us?",
        "What's something small I do that means the world to you?",
    ],
    'Future': [
        "Where do you see us in 5 years?",
        "What's one adventure you want us to go on together?",
        "What tradition do you want us to start?",
        "What does your dream home look like?",
    ],
    'Random': [
        "Would you rather have breakfast in Paris or dinner in Tokyo?",
        "What superpower would make our relationship even better?",
        "If you could describe our love in one word, what would it be?",
    ]
}


@questions_bp.route('/questions/categories', methods=['GET'])
@require_auth
def get_categories():
    return jsonify(list(QUESTION_BANK.keys()))


@questions_bp.route('/questions/random', methods=['GET'])
@require_auth
def get_random_question():
    category = request.args.get('category', 'Random')
    questions = QUESTION_BANK.get(category, QUESTION_BANK['Random'])
    question = random.choice(questions)
    return jsonify({'text': question, 'category': category})


@questions_bp.route('/questions/answer', methods=['POST'])
@require_auth
def submit_answer():
    data = request.get_json()
    try:
        current_app.supabase.table('question_answers').insert({
            'user_id': str(request.user_id),
            'question_text': data.get('questionText', ''),
            'category': data.get('category', 'Random'),
            'answer': data.get('answer', '')
        }).execute()

        # Log activity
        current_app.supabase.table('activity_feed').insert({
            'user_id': str(request.user_id),
            'action': 'answered_question',
            'icon': '💭',
            'text': "Answered today's question"
        }).execute()

        return jsonify({'message': 'Answer submitted!'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@questions_bp.route('/questions/history', methods=['GET'])
@require_auth
def get_history():
    page = int(request.args.get('page', 1))
    limit = 10
    offset = (page - 1) * limit
    try:
        result = current_app.supabase.table('question_answers') \
            .select('*') \
            .eq('user_id', request.user_id) \
            .order('created_at', desc=True) \
            .range(offset, offset + limit - 1) \
            .execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'message': str(e)}), 500
