# Hong Kong News Skill

## Description
A skill to retrieve Hong Kong-related news from RSS feeds as an alternative to web search when API keys are unavailable.

## Purpose
This skill provides Hong Kong news retrieval functionality using RSS feeds when the web_search tool is unavailable due to missing API keys.

## Commands
- `/get_hk_news` - Retrieve latest Hong Kong news from local news sources

## Implementation
Uses Python urllib to fetch RSS feeds from Hong Kong news sources and parses them to extract headlines and brief descriptions.

## Sources
- RTHK (Radio Television Hong Kong)
- SCMP (South China Morning Post)
- HKEJ (Hong Kong Economic Journal) - China section

## Limitations
- Requires internet connectivity
- Depends on RSS feed availability from news sources
- Limited to top 5 articles per source
- Some sources may have restrictions on access from certain regions