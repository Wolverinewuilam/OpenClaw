# News Skill

## Description
A skill to retrieve latest news from RSS feeds as an alternative to web search when API keys are unavailable.

## Purpose
This skill provides basic news retrieval functionality using RSS feeds when the web_search tool is unavailable due to missing API keys.

## Commands
- `/get_news` - Retrieve latest news from major news sources

## Implementation
Uses Python urllib to fetch RSS feeds from news sources and parses them to extract headlines and brief descriptions.

## Sources
- BBC News
- CNN
- Reuters

## Limitations
- Requires internet connectivity
- Depends on RSS feed availability from news sources
- Limited to top 5 articles per source