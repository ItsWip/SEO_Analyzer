import requests
import logging
import os
import time

logger = logging.getLogger(__name__)

def check_page_speed(url):
    """
    Check page speed metrics using Google PageSpeed Insights API
    Returns page speed metrics and suggestions for improvement
    """
    try:
        api_key = os.environ.get('PAGESPEED_API_KEY', '')
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile"
        if api_key:
            api_url += f"&key={api_key}"
        
        response = requests.get(api_url, timeout=30)
        
        if response.status_code != 200:
            logger.warning(f"PageSpeed API error: Status {response.status_code}")
            return {
                'error': f"PageSpeed API error: Status {response.status_code}",
                'performance_score': None,
                'first_contentful_paint': None,
                'speed_index': None,
                'largest_contentful_paint': None,
                'time_to_interactive': None,
                'total_blocking_time': None,
                'cumulative_layout_shift': None,
                'opportunities': [],
                'passed_audits': []
            }
        
        data = response.json()
        
        lighthouse_result = data.get('lighthouseResult', {})
        categories = lighthouse_result.get('categories', {})
        audits = lighthouse_result.get('audits', {})
        
        performance = categories.get('performance', {})
        performance_score = int(performance.get('score', 0) * 100) if 'score' in performance else None
        
        fcp = audits.get('first-contentful-paint', {})
        si = audits.get('speed-index', {})
        lcp = audits.get('largest-contentful-paint', {})
        tti = audits.get('interactive', {})
        tbt = audits.get('total-blocking-time', {})
        cls = audits.get('cumulative-layout-shift', {})
        
        opportunities = []
        passed_audits = []
        
        for audit_id, audit in audits.items():
            if audit.get('scoreDisplayMode') in ['informative', 'manual', 'notApplicable']:
                continue
                
            score = audit.get('score')
            
            if score is not None and score < 0.9 and 'title' in audit:
                opportunities.append({
                    'title': audit['title'],
                    'description': audit.get('description', ''),
                    'score': int(score * 100) if score is not None else 0,
                })
            elif score is not None and score >= 0.9 and 'title' in audit:
                passed_audits.append({
                    'title': audit['title'],
                    'score': int(score * 100) if score is not None else 0,
                })
        
        opportunities.sort(key=lambda x: x['score'])
        
        result = {
            'performance_score': performance_score,
            'first_contentful_paint': {
                'score': int(fcp.get('score', 0) * 100) if 'score' in fcp else None,
                'value': fcp.get('displayValue', None),
                'raw_value': fcp.get('numericValue', None),
            },
            'speed_index': {
                'score': int(si.get('score', 0) * 100) if 'score' in si else None,
                'value': si.get('displayValue', None),
                'raw_value': si.get('numericValue', None),
            },
            'largest_contentful_paint': {
                'score': int(lcp.get('score', 0) * 100) if 'score' in lcp else None,
                'value': lcp.get('displayValue', None),
                'raw_value': lcp.get('numericValue', None),
            },
            'time_to_interactive': {
                'score': int(tti.get('score', 0) * 100) if 'score' in tti else None,
                'value': tti.get('displayValue', None),
                'raw_value': tti.get('numericValue', None),
            },
            'total_blocking_time': {
                'score': int(tbt.get('score', 0) * 100) if 'score' in tbt else None,
                'value': tbt.get('displayValue', None),
                'raw_value': tbt.get('numericValue', None),
            },
            'cumulative_layout_shift': {
                'score': int(cls.get('score', 0) * 100) if 'score' in cls else None,
                'value': cls.get('displayValue', None),
                'raw_value': cls.get('numericValue', None),
            },
            'opportunities': opportunities[:5],
            'passed_audits': passed_audits[:5],
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error checking page speed for {url}: {str(e)}", exc_info=True)
        return {
            'error': str(e),
            'performance_score': None,
            'first_contentful_paint': None,
            'speed_index': None,
            'largest_contentful_paint': None,
            'time_to_interactive': None,
            'total_blocking_time': None,
            'cumulative_layout_shift': None,
            'opportunities': [],
            'passed_audits': []
        }
