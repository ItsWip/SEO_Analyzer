import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
import re

logger = logging.getLogger(__name__)

def analyze_seo(url):
    """
    Analyze basic on-page SEO elements of a webpage
    Returns a dictionary with SEO metrics and scores
    """
    try:        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string.strip() if soup.title else None
        meta_description = None
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_description_tag:
            meta_description = meta_description_tag.get('content', '')
        
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        
        canonical = None
        canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
        if canonical_tag:
            canonical = canonical_tag.get('href', '')
        
        has_viewport = bool(soup.find('meta', attrs={'name': 'viewport'}))
        
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        
        links = soup.find_all('a', href=True)
        
        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc
        
        internal_links = []
        external_links = []
        
        for link in links:
            href = link['href']
            if href.startswith('#') or not href:
                continue
                
            if href.startswith('/') or base_domain in href:
                internal_links.append(href)
            elif href.startswith(('http://', 'https://')):
                external_links.append(href)
        
        has_robots_meta = bool(soup.find('meta', attrs={'name': 'robots'}))
        
        title_length = len(title) if title else 0
        title_score = 5
        title_feedback = []
        
        if not title:
            title_score = 0
            title_feedback.append("Missing page title")
        elif title_length < 30:
            title_score = 2
            title_feedback.append("Title is too short (less than 30 characters)")
        elif title_length > 60:
            title_score = 3
            title_feedback.append("Title is too long (more than 60 characters)")
        else:
            title_score = 5
            title_feedback.append("Title length is optimal")
        
        meta_desc_length = len(meta_description) if meta_description else 0
        meta_desc_score = 5
        meta_desc_feedback = []
        
        if not meta_description:
            meta_desc_score = 0
            meta_desc_feedback.append("Missing meta description")
        elif meta_desc_length < 70:
            meta_desc_score = 2
            meta_desc_feedback.append("Meta description is too short (less than 70 characters)")
        elif meta_desc_length > 160:
            meta_desc_score = 3
            meta_desc_feedback.append("Meta description is too long (more than 160 characters)")
        else:
            meta_desc_score = 5
            meta_desc_feedback.append("Meta description length is optimal")
        
        
        heading_score = 5
        heading_feedback = []
        
        if not h1_tags:
            heading_score -= 2
            heading_feedback.append("Missing H1 heading")
        elif len(h1_tags) > 1:
            heading_score -= 1
            heading_feedback.append("Multiple H1 headings (recommended to have only one)")
        
        if not h2_tags:
            heading_score -= 1
            heading_feedback.append("Missing H2 headings")
        
        results = {
            'title': {
                'content': title,
                'length': title_length,
                'score': title_score,
                'feedback': title_feedback
            },
            'meta_description': {
                'content': meta_description,
                'length': meta_desc_length,
                'score': meta_desc_score,
                'feedback': meta_desc_feedback
            },
            'headings': {
                'h1_count': len(h1_tags),
                'h1_content': [h.get_text().strip() for h in h1_tags],
                'h2_count': len(h2_tags),
                'h3_count': len(h3_tags),
                'score': heading_score,
                'feedback': heading_feedback
            },
            'links': {
                'internal_count': len(internal_links),
                'external_count': len(external_links),
            },
            'images': {
                'total_count': len(images),
                'missing_alt_count': len(images_without_alt),
            },
            'mobile': {
                'has_viewport': has_viewport,
            },
            'overall_score': 0 
        }
        
        scores = [
            title_score,
            meta_desc_score,
            heading_score,
            5 if has_viewport else 0,
            5 if len(images_without_alt) == 0 else 3 if len(images_without_alt) < len(images)/2 else 1
        ]
        results['overall_score'] = int(sum(scores) / len(scores))
        
        recommendations = []
        
        if title_score < 4:
            for feedback in title_feedback:
                recommendations.append(f"Title: {feedback}")
                
        if meta_desc_score < 4:
            for feedback in meta_desc_feedback:
                recommendations.append(f"Meta Description: {feedback}")
                
        if heading_score < 4:
            for feedback in heading_feedback:
                recommendations.append(f"Headings: {feedback}")
                
        if len(images_without_alt) > 0:
            recommendations.append(f"Add alt text to {len(images_without_alt)} images for better accessibility and SEO")
            
        if not has_viewport:
            recommendations.append("Add a viewport meta tag for mobile responsiveness")
            
        if len(internal_links) < 5:
            recommendations.append("Add more internal links to improve site structure")
            
        results['recommendations'] = recommendations
        
        return results
        
    except Exception as e:
        logger.error(f"Error analyzing SEO for {url}: {str(e)}", exc_info=True)
        return {
            'error': str(e),
            'title': {'content': None, 'score': 0},
            'meta_description': {'content': None, 'score': 0},
            'headings': {'h1_count': 0, 'score': 0},
            'overall_score': 0,
            'recommendations': ["Could not analyze page due to error"]
        }
