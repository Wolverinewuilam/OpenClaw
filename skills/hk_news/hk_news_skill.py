#!/usr/bin/env python3
"""
Hong Kong news retrieval skill using official Hong Kong government RSS feeds
"""

import urllib.request
import urllib.parse
from xml.etree import ElementTree as ET
import json
from datetime import datetime

def get_hk_news():
    """Retrieve Hong Kong news from official RSS feeds"""
    hk_sources = {
        'HK News Ticker': 'https://www.news.gov.hk/en/common/html/ticker.rss.xml',
        'HK Top Stories': 'https://www.news.gov.hk/en/common/html/topstories.rss.xml',
        'HK Administration & Civic Affairs': 'https://www.news.gov.hk/en/categories/admin/html/articlelist.rss.xml',
        'HK Business & Finance': 'https://www.news.gov.hk/en/categories/finance/html/articlelist.rss.xml',
        'HK City Life': 'https://www.news.gov.hk/en/city_life/html/articlelist.rss.xml',
        'HK Environment': 'https://www.news.gov.hk/en/categories/environment/html/articlelist.rss.xml',
        'HK Health & Community': 'https://www.news.gov.hk/en/categories/health/html/articlelist.rss.xml',
        'HK Law & Order': 'https://www.news.gov.hk/en/categories/law_order/html/articlelist.rss.xml',
        'HK All Press Releases': 'https://www.info.gov.hk/gia/rss/general_en.xml',
        'RTHK Local News': 'https://rthk.hk/rthk/news/rss/e_expressnews_elocal.xml',
        'RTHK Greater China News': 'https://rthk.hk/rthk/news/rss/e_expressnews_egreaterchina.xml',
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

def get_hk_weather():
    """Retrieve Hong Kong weather information"""
    weather_sources = {
        'Weather Warning Summary': 'https://rss.weather.gov.hk/rss/WeatherWarningSummaryv2.xml',
        'Local Weather Forecast': 'https://rss.weather.gov.hk/rss/LocalWeatherForecast.xml',
    }
    
    weather_results = {}
    for source_name, rss_url in weather_sources.items():
        try:
            req = urllib.request.Request(
                rss_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw HK Weather Skill)'
                }
            )
            response = urllib.request.urlopen(req, timeout=10)
            content = response.read().decode('utf-8')
            
            # Parse RSS feed
            root = ET.fromstring(content)
            items = []
            
            for item in root.findall('.//item')[:2]:  # Get top 2 weather updates
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
            
            weather_results[source_name] = items
        except Exception as e:
            weather_results[source_name] = [{'error': str(e)}]
    
    return weather_results

if __name__ == "__main__":
    # Get Hong Kong news
    hk_news = get_hk_news()
    print("Hong Kong News:")
    print(json.dumps(hk_news, indent=2, default=str))
    
    print("\nHong Kong Weather:")
    # Get Hong Kong weather
    hk_weather = get_hk_weather()
    print(json.dumps(hk_weather, indent=2, default=str))