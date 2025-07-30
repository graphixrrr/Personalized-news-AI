import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, Dict
import time
import random

class ContentFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def fetch_full_content(self, url: str) -> Optional[str]:
        """Fetch full article content from URL"""
        try:
            # Add delay to be respectful to servers
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try different content extraction strategies
            content = self._extract_content(soup, url)
            
            if content:
                # Clean up the content
                content = self._clean_content(content)
                return content
                
        except Exception as e:
            print(f"Error fetching content from {url}: {e}")
            
        return None
    
    def _extract_content(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        """Extract article content using multiple strategies"""
        
        # Strategy 1: Look for common article content selectors
        content_selectors = [
            'article',
            '[class*="article"]',
            '[class*="content"]',
            '[class*="post"]',
            '[class*="story"]',
            '.entry-content',
            '.post-content',
            '.article-content',
            '.story-content',
            '#content',
            '#article-content',
            '.content-body',
            '.article-body',
            '.post-body'
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # Find the largest element (likely the main content)
                largest_element = max(elements, key=lambda x: len(x.get_text()))
                if len(largest_element.get_text()) > 500:  # Minimum content length
                    return largest_element.get_text()
        
        # Strategy 2: Look for paragraphs with substantial text
        paragraphs = soup.find_all('p')
        if paragraphs:
            # Filter paragraphs with substantial content
            content_paragraphs = [p.get_text().strip() for p in paragraphs 
                                if len(p.get_text().strip()) > 100]
            
            if content_paragraphs:
                return '\n\n'.join(content_paragraphs)
        
        # Strategy 3: Extract from main content area
        main_selectors = ['main', '#main', '.main', '[role="main"]']
        for selector in main_selectors:
            main = soup.select_one(selector)
            if main:
                text = main.get_text()
                if len(text) > 500:
                    return text
        
        # Strategy 4: Fallback to body content
        body = soup.find('body')
        if body:
            text = body.get_text()
            if len(text) > 1000:
                return text
        
        return None
    
    def _clean_content(self, content: str) -> str:
        """Clean and format the extracted content"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove common unwanted text
        unwanted_patterns = [
            r'Subscribe.*?newsletter',
            r'Sign up.*?updates',
            r'Follow us.*?social',
            r'Share this.*?article',
            r'Read more.*?stories',
            r'Advertisement',
            r'Advertise',
            r'Cookie Policy',
            r'Privacy Policy',
            r'Terms of Service',
            r'Contact Us',
            r'About Us',
            r'Home',
            r'Menu',
            r'Search',
            r'Login',
            r'Register',
            r'Subscribe',
            r'Follow',
            r'Share',
            r'Comment',
            r'Like',
            r'Share on Facebook',
            r'Share on Twitter',
            r'Share on LinkedIn'
        ]
        
        for pattern in unwanted_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Remove extra whitespace again
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        # Limit content length to reasonable size
        if len(content) > 10000:
            content = content[:10000] + "..."
        
        return content
    
    def get_article_metadata(self, url: str) -> Dict:
        """Extract article metadata (title, author, date) from URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            metadata = {
                'title': None,
                'author': None,
                'published_date': None,
                'description': None
            }
            
            # Extract title
            title_selectors = [
                'h1',
                '[property="og:title"]',
                '[name="twitter:title"]',
                'title'
            ]
            
            for selector in title_selectors:
                element = soup.select_one(selector)
                if element:
                    if selector in ['[property="og:title"]', '[name="twitter:title"]']:
                        metadata['title'] = element.get('content', '').strip()
                    else:
                        metadata['title'] = element.get_text().strip()
                    if metadata['title']:
                        break
            
            # Extract author
            author_selectors = [
                '[rel="author"]',
                '[class*="author"]',
                '[class*="byline"]',
                '[property="article:author"]'
            ]
            
            for selector in author_selectors:
                element = soup.select_one(selector)
                if element:
                    metadata['author'] = element.get_text().strip()
                    break
            
            # Extract description
            desc_selectors = [
                '[property="og:description"]',
                '[name="description"]',
                '[name="twitter:description"]'
            ]
            
            for selector in desc_selectors:
                element = soup.select_one(selector)
                if element:
                    metadata['description'] = element.get('content', '').strip()
                    break
            
            return metadata
            
        except Exception as e:
            print(f"Error extracting metadata from {url}: {e}")
            return {'title': None, 'author': None, 'published_date': None, 'description': None} 