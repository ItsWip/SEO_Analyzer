import requests
from bs4 import BeautifulSoup
import re
import logging
import trafilatura
from collections import Counter
import string
import math

logger = logging.getLogger(__name__)

def analyze_content(url):
    """
    Analyze the content of a webpage for SEO
    Returns a dictionary with content metrics and scores
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        downloaded = trafilatura.fetch_url(url)
        text_content = trafilatura.extract(downloaded)
        
        if not text_content:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script_or_style in soup(['script', 'style', 'nav', 'footer', 'header']):
                script_or_style.decompose()
            text_content = soup.get_text(separator=' ', strip=True)
        
        word_count = len(text_content.split())
        paragraph_count = len(re.split(r'\n\s*\n', text_content))
        
        words = re.findall(r'\b[a-zA-Z]{3,15}\b', text_content.lower())
        stop_words = {'the', 'and', 'are', 'for', 'was', 'with', 'this', 'that', 'from', 'they', 'were', 'have', 'what', 'your', 'will', 'been'}
        filtered_words = [word for word in words if word not in stop_words]
        
        word_freq = Counter(filtered_words)
        total_words = len(filtered_words)
        
        top_keywords = []
        if total_words > 0:
            for word, count in word_freq.most_common(10):
                density = (count / total_words) * 100
                top_keywords.append({
                    'word': word,
                    'count': count,
                    'density': round(density, 2)
                })
        
        sentences = re.split(r'[.!?]+', text_content)
        sentence_count = len([s for s in sentences if len(s.strip()) > 0])
        
        if sentence_count == 0 or word_count == 0:
            readability_score = 0
        else:
            avg_sentence_length = word_count / sentence_count
            
            def count_syllables(word):
                word = word.lower()
                if len(word) <= 3:
                    return 1
                    
                if word.endswith('es') or word.endswith('ed'):
                    word = word[:-2]
                elif word.endswith('e'):
                    word = word[:-1]
                    
                vowels = 'aeiouy'
                count = 0
                prev_is_vowel = False
                
                for char in word:
                    is_vowel = char in vowels
                    if is_vowel and not prev_is_vowel:
                        count += 1
                    prev_is_vowel = is_vowel
                    
                return max(1, count)
            
            syllable_count = sum(count_syllables(word) for word in text_content.split())
            
            avg_syllables_per_word = syllable_count / word_count
            
            readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            
            readability_score = max(0, min(100, readability_score))
        
        readability_level = ""
        if readability_score >= 90:
            readability_level = "Very Easy"
        elif readability_score >= 80:
            readability_level = "Easy"
        elif readability_score >= 70:
            readability_level = "Fairly Easy"
        elif readability_score >= 60:
            readability_level = "Standard"
        elif readability_score >= 50:
            readability_level = "Fairly Difficult"
        elif readability_score >= 30:
            readability_level = "Difficult"
        else:
            readability_level = "Very Difficult"
        
        content_score = 0
        content_feedback = []
        
        if word_count < 300:
            content_score += 1
            content_feedback.append("Content is too short (less than 300 words)")
        elif word_count < 600:
            content_score += 2
            content_feedback.append("Content is somewhat short (300-600 words)")
        elif word_count < 1200:
            content_score += 4
            content_feedback.append("Content has a good length (600-1200 words)")
        else:
            content_score += 5
            content_feedback.append("Content has excellent length (1200+ words)")
        

        if readability_score < 30:
            content_score += 1
            content_feedback.append("Content is very difficult to read")
        elif readability_score < 50:
            content_score += 2
            content_feedback.append("Content is difficult to read")
        elif readability_score < 70:
            content_score += 4
            content_feedback.append("Content has standard readability")
        else:
            content_score += 5
            content_feedback.append("Content has excellent readability")
        
        if not top_keywords:
            content_score += 0
            content_feedback.append("No clear focus keywords identified")
        else:
            top_keyword_density = top_keywords[0]['density'] if top_keywords else 0
            
            if top_keyword_density > 5:
                content_score += 2
                content_feedback.append("Possible keyword stuffing detected")
            elif top_keyword_density > 3:
                content_score += 5
                content_feedback.append("Good keyword density")
            elif top_keyword_density > 1:
                content_score += 4
                content_feedback.append("Acceptable keyword density")
            else:
                content_score += 2
                content_feedback.append("Low keyword density")
        
        content_score = min(5, content_score / 3)
        
        recommendations = []
        
        if word_count < 600:
            recommendations.append(f"Increase content length (currently {word_count} words, aim for 600+ words)")
            
        if readability_score < 50:
            recommendations.append("Simplify content to improve readability (use shorter sentences and simpler words)")
            
        if top_keyword_density > 5:
            recommendations.append("Reduce keyword density to avoid keyword stuffing")
        elif top_keyword_density < 1 and word_count > 300:
            recommendations.append("Increase usage of target keywords to improve relevance")
        
        result = {
            'word_count': word_count,
            'paragraph_count': paragraph_count,
            'sentence_count': sentence_count,
            'top_keywords': top_keywords,
            'readability': {
                'score': round(readability_score, 1),
                'level': readability_level,
            },
            'content_score': round(content_score, 1),
            'feedback': content_feedback,
            'recommendations': recommendations
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing content for {url}: {str(e)}", exc_info=True)
        return {
            'error': str(e),
            'word_count': 0,
            'top_keywords': [],
            'readability': {'score': 0, 'level': 'Unknown'},
            'content_score': 0,
            'feedback': ["Could not analyze content due to error"],
            'recommendations': ["Fix website access issues to enable content analysis"]
        }
