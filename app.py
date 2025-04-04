import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from urllib.parse import urlparse
import time

from seo.analyzer import analyze_seo
from seo.page_speed import check_page_speed
from seo.content import analyze_content
from seo.competitors import compare_with_competitors

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

seo_results_cache = {}

@app.route('/')
def index():
    """Render the main page with the URL input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process the URL and perform SEO analysis"""
    try:
        url = request.form.get('url', '').strip()
        competitor_url = request.form.get('competitor_url', '').strip()
        
        if not url:
            return render_template('index.html', error="Please enter a valid URL")
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        parsed_url = urlparse(url)
        if not parsed_url.netloc:
            return render_template('index.html', error="Invalid URL format")

        cache_key = f"{url}_{competitor_url}"
        current_time = time.time()
        if cache_key in seo_results_cache and current_time - seo_results_cache[cache_key]['timestamp'] < 1800:
            logger.debug(f"Using cached results for {url}")
            results = seo_results_cache[cache_key]['data']
        else:
            logger.debug(f"Analyzing URL: {url}")
            
            basic_seo = analyze_seo(url)
            content_analysis = analyze_content(url)
            speed_results = check_page_speed(url)
            
            competitor_analysis = None
            if competitor_url:
                if not competitor_url.startswith(('http://', 'https://')):
                    competitor_url = 'https://' + competitor_url
                competitor_analysis = compare_with_competitors(url, competitor_url)
            
            results = {
                'url': url,
                'basic_seo': basic_seo,
                'content_analysis': content_analysis,
                'speed_results': speed_results,
                'competitor_analysis': competitor_analysis,
                'competitor_url': competitor_url
            }
            
            seo_results_cache[cache_key] = {
                'data': results,
                'timestamp': current_time
            }
            
        session['seo_results'] = results
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        return render_template('index.html', error=f"An error occurred: {str(e)}")

@app.route('/competitor-analysis')
def competitor_analysis():
    """Show detailed competitor analysis"""
    results = session.get('seo_results')
    if not results or not results.get('competitor_analysis'):
        return redirect(url_for('index'))
    
    return render_template('competitor_analysis.html', results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html', error="Server error occurred. Please try again later."), 500
