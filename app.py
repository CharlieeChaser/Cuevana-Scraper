from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== Health Check ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Cuevana Scraper API'
    }), 200


# ==================== Search Endpoints ====================
@app.route('/api/search', methods=['GET'])
def search():
    """
    Search for movies/shows on Cuevana.
    
    Query Parameters:
    - query (required): Search term
    - type (optional): 'movie' or 'show' (default: all)
    - page (optional): Page number (default: 1)
    """
    try:
        query = request.args.get('query', '').strip()
        search_type = request.args.get('type', 'all')
        page = request.args.get('page', 1, type=int)
        
        if not query:
            return jsonify({
                'error': 'Query parameter is required',
                'message': 'Please provide a search term'
            }), 400
        
        if search_type not in ['all', 'movie', 'show']:
            return jsonify({
                'error': 'Invalid type parameter',
                'message': "Type must be 'all', 'movie', or 'show'"
            }), 400
        
        # Placeholder for actual scraping logic
        results = {
            'query': query,
            'type': search_type,
            'page': page,
            'results': [],
            'total_results': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Search request - Query: {query}, Type: {search_type}, Page: {page}")
        
        return jsonify(results), 200
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({
            'error': 'Search failed',
            'message': str(e)
        }), 500


@app.route('/api/search/<search_id>', methods=['GET'])
def get_search_details(search_id):
    """
    Get detailed information about a specific search result.
    
    Path Parameters:
    - search_id: ID of the search result
    """
    try:
        if not search_id:
            return jsonify({
                'error': 'Invalid search ID',
                'message': 'Search ID is required'
            }), 400
        
        details = {
            'id': search_id,
            'title': '',
            'description': '',
            'genre': [],
            'rating': 0,
            'release_date': '',
            'cast': [],
            'links': [],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Details request - Search ID: {search_id}")
        
        return jsonify(details), 200
        
    except Exception as e:
        logger.error(f"Details retrieval error: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve details',
            'message': str(e)
        }), 500


# ==================== Category Endpoints ====================
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Get available categories/genres.
    """
    try:
        categories = {
            'categories': [
                'Action',
                'Comedy',
                'Drama',
                'Horror',
                'Thriller',
                'Romance',
                'Animation',
                'Sci-Fi',
                'Adventure'
            ],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info("Categories request")
        
        return jsonify(categories), 200
        
    except Exception as e:
        logger.error(f"Categories retrieval error: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve categories',
            'message': str(e)
        }), 500


@app.route('/api/categories/<category>', methods=['GET'])
def get_category_items(category):
    """
    Get all items in a specific category.
    
    Path Parameters:
    - category: Category name
    
    Query Parameters:
    - page (optional): Page number (default: 1)
    """
    try:
        page = request.args.get('page', 1, type=int)
        
        items = {
            'category': category,
            'page': page,
            'items': [],
            'total_items': 0,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Category items request - Category: {category}, Page: {page}")
        
        return jsonify(items), 200
        
    except Exception as e:
        logger.error(f"Category items retrieval error: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve category items',
            'message': str(e)
        }), 500


# ==================== Trending Endpoints ====================
@app.route('/api/trending', methods=['GET'])
def get_trending():
    """
    Get trending movies and shows.
    
    Query Parameters:
    - type (optional): 'movie' or 'show' (default: all)
    - limit (optional): Number of results (default: 10, max: 50)
    """
    try:
        search_type = request.args.get('type', 'all')
        limit = request.args.get('limit', 10, type=int)
        
        if search_type not in ['all', 'movie', 'show']:
            return jsonify({
                'error': 'Invalid type parameter',
                'message': "Type must be 'all', 'movie', or 'show'"
            }), 400
        
        if limit < 1 or limit > 50:
            limit = 10
        
        trending = {
            'type': search_type,
            'limit': limit,
            'items': [],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Trending request - Type: {search_type}, Limit: {limit}")
        
        return jsonify(trending), 200
        
    except Exception as e:
        logger.error(f"Trending retrieval error: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve trending items',
            'message': str(e)
        }), 500


# ==================== Error Handlers ====================
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist',
        'status_code': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'status_code': 500
    }), 500


# ==================== Main ====================
if __name__ == '__main__':
    logger.info("Starting Cuevana Scraper API")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
