from flask import Blueprint, jsonify
from ..models.user import db

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'

    health_status = {
        'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
        'database': db_status,
        'api_version': '1.0.0'
    }
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code
