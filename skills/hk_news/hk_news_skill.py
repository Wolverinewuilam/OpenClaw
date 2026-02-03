#!/usr/bin/env python3
"""
Hong Kong news retrieval skill using RSS feeds
"""

import urllib.request
import urllib.parse
from xml.etree import ElementTree as ET
import json
from datetime import datetime

def get_hk_news():
    """Retrieve Hong Kong news from RSS feeds"""
    hk_sources = {
        'Apple Daily Archive': 'https://hk.apple.nextmedia.com/rss/hongkong/local.xml',  # Alternative HK news source
        'Sing Tao News': 'https://std.stheadline.com/rss/generic/en/all.xml',  # English section
        'Oriental Daily': 'https://orientaldaily.on.cc/rss/news.xml',  # Possible alternative
    }
    
    news_results = {}
    for source_name, rss_url in hk_sources.items():
        try:
            req = urllib.request.Request(
                rss_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw HK News Skill)'
                }
            )
            response = urllib.request.urlopen(req, timeout=10)
            content = response.read().decode('utf-8')
            
            # Parse RSS feed
            root = ET.fromstring(content)
            items = []
            
            for item in root.findall('.//item')[:3]:  # Get top 3 articles
                title = item.find('title').text if item.find('title') is not None else 'No Title'
                description = item.find('description').text if item.find('description') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                # Clean description
                if description:
                    import re
                    description = re.sub('<[^<]+?>', '', description)
                    description = description[:200] + '...' if len(description) > 200 else description
                
                items.append({
                    'title': title,
                    'description': description,
                    'pub_date': pub_date
                })
            
            news_results[source_name] = items
        except Exception as e:
            news_results[source_name] = [{'error': str(e)}]
    
    return news_results

def get_international_news_with_hk_focus():
    """Alternative: Get international news that might include HK topics"""
    sources = {
        'BBC Asia': 'http://feeds.bbci.co.uk/news/world/asia/rss.xml',
        'Reuters Asia': 'http://feeds.reuters.com/reuters/AsiaPacificNews',
    }
    
    news_results = {}
    for source_name, rss_url in sources.items():
        try:
            req = urllib.request.Request(
                rss_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw HK News Skill)'
                }
            )
            response = urllib.request.urlopen(req, timeout=10)
            content = response.read().decode('utf-8')
            
            # Parse RSS feed
            root = ET.fromstring(content)
            items = []
            
            # Filter for HK-related content or just get general Asia news
            for item in root.findall('.//item')[:3]:
                title = item.find('title').text if item.find('title') is not None else 'No Title'
                description = item.find('description').text if item.find('description') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                
                # Check if title or description contains HK-related terms
                hk_related = ('Hong Kong' in title or 'Hong Kong' in description or 
                             'China' in title or 'China' in description or
                             'HK' in title or 'HK' in description)
                
                # Clean description
                if description:
                    import re
                    description = re.sub('<[^<]+?>', '', description)
                    description = description[:200] + '...' if len(description) > 200 else description
                
                items.append({
                    'title': title,
                    'description': description,
                    'pub_date': pub_date,
                    'hk_related': hk_related
                })
            
            news_results[source_name] = items
        except Exception as e:
            news_results[source_name] = [{'error': str(e)}]
    
    return news_results

if __name__ == "__main__":
    # Try Hong Kong specific sources first
    hk_news = get_hk_news()
    print("Hong Kong News:")
    print(json.dumps(hk_news, indent=2, default=str))
    
    print("\nAsia/HK Related News:")
    # Then try Asia-focused international sources
    asia_news = get_international_news_with_hk_focus()
    print(json.dumps(asia_news, indent=2, default=str))