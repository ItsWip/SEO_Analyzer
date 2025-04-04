import re
from urllib.parse import urlparse, urljoin


def is_valid_url(url):
    """Check if URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def normalize_url(url):
    """Normalize URL by adding scheme if missing"""
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url


def get_domain(url):
    """Extract domain from URL"""
    parsed_url = urlparse(url)
    return parsed_url.netloc


def make_absolute_url(base_url, relative_url):
    """Convert relative URL to absolute URL"""
    return urljoin(base_url, relative_url)


def extract_keywords_from_text(text, stop_words=None):
    """Extract keywords from text and remove stop words"""
    if stop_words is None:
        stop_words = {'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'with', 'on', 'as', 'by', 'at', 'an', 'be', 
                       'are', 'this', 'that', 'it', 'from', 'or', 'was', 'were', 'has', 'have', 'had', 'but', 'not', 
                       'what', 'all', 'can', 'when', 'which', 'their', 'will', 'if', 'more', 'about', 'after', 'before'}
    
    # Remove punctuation and convert to lowercase
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Split into words
    words = text.split()
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords


def calculate_keyword_density(keywords, total_words):
    """Calculate keyword density as a percentage"""
    if total_words == 0:
        return 0
    return (keywords / total_words) * 100


def calculate_readability_score(text):
    """
    Calculate Flesch Reading Ease score
    Formula: 206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)
    """
    # Count words
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    # Count sentences (approximate)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if len(s.strip()) > 0])
    
    if sentence_count == 0 or word_count == 0:
        return 0
    
    # Approximate syllable count (this is a simplification)
    def count_syllables(word):
        word = word.lower()
        if len(word) <= 3:
            return 1
        
        # Count vowel groups as syllables
        count = 0
        vowels = 'aeiouy'
        prev_is_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_vowel
        
        # Handle common word endings
        if word.endswith('e') and not word.endswith('le'):
            count -= 1
        
        return max(1, count)  # Every word has at least one syllable
    
    syllable_count = sum(count_syllables(word) for word in words)
    
    # Calculate averages
    avg_sentence_length = word_count / sentence_count
    avg_syllables_per_word = syllable_count / word_count
    
    # Apply Flesch Reading Ease formula
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    
    # Ensure score is within bounds
    return max(0, min(100, score))


def get_readability_level(score):
    """Convert Flesch Reading Ease score to difficulty level"""
    if score >= 90:
        return "Very Easy"
    elif score >= 80:
        return "Easy"
    elif score >= 70:
        return "Fairly Easy"
    elif score >= 60:
        return "Standard"
    elif score >= 50:
        return "Fairly Difficult"
    elif score >= 30:
        return "Difficult"
    else:
        return "Very Difficult"
