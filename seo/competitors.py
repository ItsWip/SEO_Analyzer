import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
from seo.analyzer import analyze_seo
from seo.content import analyze_content
from seo.page_speed import check_page_speed

logger = logging.getLogger(__name__)

def compare_with_competitors(main_url, competitor_url):
    """
    Compare the main website with a competitor website
    Returns a dictionary with comparative metrics
    """
    try:
        main_seo = analyze_seo(main_url)
        competitor_seo = analyze_seo(competitor_url)
        
        main_content = analyze_content(main_url)
        competitor_content = analyze_content(competitor_url)
        
        if 'error' not in main_seo and 'error' not in competitor_seo:
            main_speed = check_page_speed(main_url)
            competitor_speed = check_page_speed(competitor_url)
        else:
            main_speed = {'performance_score': None}
            competitor_speed = {'performance_score': None}
        
        main_domain = urlparse(main_url).netloc
        competitor_domain = urlparse(competitor_url).netloc
        
        comparison = {
            'domains': {
                'main': main_domain,
                'competitor': competitor_domain
            },
            'seo_scores': {
                'main': main_seo.get('overall_score', 0),
                'competitor': competitor_seo.get('overall_score', 0)
            },
            'content_scores': {
                'main': main_content.get('content_score', 0),
                'competitor': competitor_content.get('content_score', 0)
            },
            'performance_scores': {
                'main': main_speed.get('performance_score', 0),
                'competitor': competitor_speed.get('performance_score', 0)
            },
            'word_counts': {
                'main': main_content.get('word_count', 0),
                'competitor': competitor_content.get('word_count', 0)
            },
            'readability': {
                'main': main_content.get('readability', {}).get('score', 0),
                'competitor': competitor_content.get('readability', {}).get('score', 0)
            },
            'title_length': {
                'main': main_seo.get('title', {}).get('length', 0),
                'competitor': competitor_seo.get('title', {}).get('length', 0)
            },
            'meta_desc_length': {
                'main': main_seo.get('meta_description', {}).get('length', 0),
                'competitor': competitor_seo.get('meta_description', {}).get('length', 0)
            },
            'headings': {
                'main': {
                    'h1': main_seo.get('headings', {}).get('h1_count', 0),
                    'h2': main_seo.get('headings', {}).get('h2_count', 0),
                    'h3': main_seo.get('headings', {}).get('h3_count', 0)
                },
                'competitor': {
                    'h1': competitor_seo.get('headings', {}).get('h1_count', 0),
                    'h2': competitor_seo.get('headings', {}).get('h2_count', 0),
                    'h3': competitor_seo.get('headings', {}).get('h3_count', 0)
                }
            },
            'keyword_overlap': []
        }
        
        main_keywords = {kw['word']: kw['density'] for kw in main_content.get('top_keywords', [])}
        competitor_keywords = {kw['word']: kw['density'] for kw in competitor_content.get('top_keywords', [])}
        
        common_keywords = set(main_keywords.keys()) & set(competitor_keywords.keys())
        
        for keyword in common_keywords:
            comparison['keyword_overlap'].append({
                'keyword': keyword,
                'main_density': main_keywords[keyword],
                'competitor_density': competitor_keywords[keyword]
            })
        
        comparison['keyword_overlap'].sort(key=lambda x: x['competitor_density'], reverse=True)
        
        insights = []
        
        if comparison['seo_scores']['main'] < comparison['seo_scores']['competitor']:
            insights.append(f"Competitor has a better overall SEO score ({comparison['seo_scores']['competitor']} vs {comparison['seo_scores']['main']})")
        
        main_wc = comparison['word_counts']['main']
        competitor_wc = comparison['word_counts']['competitor']
        
        if main_wc < competitor_wc:
            insights.append(f"Competitor has more content ({competitor_wc} words vs {main_wc} words)")
        
        if (comparison['performance_scores']['main'] is not None and 
            comparison['performance_scores']['competitor'] is not None and
            comparison['performance_scores']['main'] < comparison['performance_scores']['competitor']):
            insights.append(f"Competitor has better page performance score ({comparison['performance_scores']['competitor']} vs {comparison['performance_scores']['main']})")
        
        if comparison['keyword_overlap']:
            better_kw_count = 0
            for kw in comparison['keyword_overlap']:
                if kw['competitor_density'] > kw['main_density']:
                    better_kw_count += 1
            
            if better_kw_count > len(comparison['keyword_overlap']) / 2:
                insights.append(f"Competitor uses {better_kw_count} common keywords more effectively")
        
        recommendations = []
        
        if main_wc < competitor_wc:
            recommendations.append(f"Increase content length to match or exceed competitor's {competitor_wc} words")
        
        if (comparison['title_length']['main'] < comparison['title_length']['competitor'] and 
            comparison['title_length']['competitor'] <= 60):
            recommendations.append("Optimize title tag length to match competitor's more descriptive title")
        
        if (comparison['meta_desc_length']['main'] < comparison['meta_desc_length']['competitor'] and 
            comparison['meta_desc_length']['competitor'] <= 160):
            recommendations.append("Improve meta description to match competitor's more detailed description")
        
        if comparison['keyword_overlap']:
            potential_keywords = [kw['keyword'] for kw in comparison['keyword_overlap'] 
                                 if kw['competitor_density'] > kw['main_density']]
            if potential_keywords:
                recommendations.append(f"Consider optimizing for these competitor keywords: {', '.join(potential_keywords[:3])}")
        
        comparison['insights'] = insights
        comparison['recommendations'] = recommendations
        
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing websites: {str(e)}", exc_info=True)
        return {
            'error': str(e),
            'domains': {
                'main': urlparse(main_url).netloc,
                'competitor': urlparse(competitor_url).netloc
            },
            'insights': ["Could not complete competitor analysis due to error"],
            'recommendations': ["Fix website access issues to enable competitor analysis"]
        }
