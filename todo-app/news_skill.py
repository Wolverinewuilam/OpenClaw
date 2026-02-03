#!/usr/bin/env python3
"""
Basic news retrieval skill using RSS feeds
This is a workaround for missing web search API
"""

import urllib.request
import urllib.parse
from xml.etree import ElementTree as ET
import json
from datetime import datetime

def get_news_from_rss(rss_url):
    """Retrieve news from RSS feed"""
    try:
        req = urllib.request.Request(
            rss_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw News Skill)'
            }
        )
        response = urllib.request.urlopen(req, timeout=10)
        content = response.read().decode('utf-8')
        
        # Parse RSS feed
        root = ET.fromstring(content)
        items = []
        
        for item in root.findall('.//item')[:5]:  # Get top 5 articles
            title = item.find('title').text if item.find('title') is not None else 'No Title'
            description = item.find('description').text if item.find('description') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            
            # Clean description
            if description:
                # Remove HTML tags if present
                import re
                description = re.sub('<[^<]+?>', '', description)
                description = description[:200] + '...' if len(description) > 200 else description
            
            items.append({
                'title': title,
                'description': description,
                'pub_date': pub_date
            })
        
        return items
    except Exception as e:
        return [{'error': str(e)}]

def get_top_news():
    """Get top news from various sources"""
    sources = {
        'BBC News': 'http://feeds.bbci.co.uk/news/rss.xml',
        'CNN': 'http://rss.cnn.com/rss/edition.rss',
        'Reuters': 'http://feeds.reuters.com/reuters/topNews',
    }
    
    news_results = {}
    for source_name, rss_url in sources.items():
        news_results[source_name] = get_news_from_rss(rss_url)
    
    return news_results

if __name__ == "__main__":
    # Test the function
    news = get_top_news()
    print(json.dumps(news, indent=2, default=str))