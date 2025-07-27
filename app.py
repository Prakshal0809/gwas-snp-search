import os
import threading
import time
from flask import Flask, render_template, request, jsonify, send_file
from gwas_scraper import run_gwas_scrape

app = Flask(__name__)

# Global status tracking
scraping_status = {
    'is_running': False,
    'progress': 0,
    'message': '',
    'filename': '',
    'error': None,
    'count': 0,
    'skipped_count': 0,
    'pages_scraped': 0
}

def run_scraping_task(search_term):
    """Run the scraping task in a background thread"""
    global scraping_status
    
    scraping_status.update({
        'is_running': True,
        'progress': 0,
        'message': 'Starting...',
        'filename': '',
        'error': None,
        'count': 0,
        'skipped_count': 0,
        'pages_scraped': 0
    })
    
    def progress_callback(progress, message):
        scraping_status['progress'] = progress
        scraping_status['message'] = message
    
    try:
        # Run the scraper with a 15-minute timeout
        start_time = time.time()
        timeout = 15 * 60  # 15 minutes
        
        result = run_gwas_scrape(search_term, progress_callback, max_pages=None)
        
        # Check if we exceeded timeout
        if time.time() - start_time > timeout:
            scraping_status.update({
                'is_running': False,
                'progress': 100,
                'message': 'Search timed out after 15 minutes',
                'error': 'Timeout exceeded'
            })
            return
        
        if result['success']:
            # Check if no results were found
            if result.get('no_results', False):
                scraping_status.update({
                    'is_running': False,
                    'progress': 100,
                    'message': f'No results found for search term "{search_term}"',
                    'filename': '',
                    'count': 0,
                    'skipped_count': 0,
                    'pages_scraped': 0,
                    'error': None,
                    'no_results': True
                })
            else:
                scraping_status.update({
                    'is_running': False,
                    'progress': 100,
                    'message': f'Completed! Found {result["count"]} SNPs',
                    'filename': result['filename'],
                    'count': result['count'],
                    'skipped_count': result['skipped_count'],
                    'pages_scraped': result['pages_scraped'],
                    'error': None
                })
        else:
            scraping_status.update({
                'is_running': False,
                'progress': 100,
                'message': 'Search failed',
                'error': result['error']
            })
            
    except Exception as e:
        scraping_status.update({
            'is_running': False,
            'progress': 100,
            'message': 'Search failed',
            'error': str(e)
        })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'error': 'A search is already in progress'}), 400
    
    data = request.get_json()
    search_term = data.get('search_term', '').strip()
    
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400
    
    # Start scraping in background thread
    thread = threading.Thread(target=run_scraping_task, args=(search_term,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Search started successfully'})

@app.route('/api/status')
def status():
    return jsonify(scraping_status)

@app.route('/api/download/<filename>')
def download(filename):
    try:
        downloads_dir = "downloads"
        filepath = os.path.join(downloads_dir, filename)
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # Use environment variables for Render deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 