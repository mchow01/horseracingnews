import requests
import xml.etree.ElementTree as ET
from html import unescape
import re
from typing import List, Dict, Any
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Thoroughbred Daily News")

def clean_html(text: str) -> str:
    """Remove HTML tags and decode HTML entities from text."""
    if not text:
        return ""
    
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    
    # Decode HTML entities
    text = unescape(text)
    
    # Clean up extra whitespace
    text = ' '.join(text.split())
    
    return text

def parse_rss_feed(url: str) -> Dict[str, Any]:
    """Fetch and parse RSS feed, returning structured data."""
    try:
        # Fetch the RSS feed
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the XML
        root = ET.fromstring(response.content)
        
        # Find the channel element
        channel = root.find('channel')
        if channel is None:
            return {"error": "Could not find channel element in RSS feed"}
        
        # Extract feed metadata
        feed_info = {
            "title": channel.find('title').text if channel.find('title') is not None else "N/A",
            "description": channel.find('description').text if channel.find('description') is not None else "N/A",
            "link": channel.find('link').text if channel.find('link') is not None else "N/A"
        }
        
        # Find all item elements
        items = channel.findall('item')
        
        stories = []
        for item in items:
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            pub_date = item.find('pubDate')
            
            story = {
                "title": clean_html(title.text) if title is not None else "No title available",
                "content": clean_html(description.text) if description is not None else "No content available",
                "link": link.text if link is not None else "No link available",
                "published": pub_date.text if pub_date is not None else "No date available"
            }
            stories.append(story)
        
        return {
            "feed_info": feed_info,
            "stories": stories,
            "total_stories": len(stories)
        }
    
    except requests.RequestException as e:
        return {"error": f"Error fetching RSS feed: {str(e)}"}
    except ET.ParseError as e:
        return {"error": f"Error parsing XML: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@mcp.tool()
def get_horse_racing_news(limit: int = 10) -> Dict[str, Any]:
    """
    Fetch the latest horse racing news from Thoroughbred Daily News.
    
    Args:
        limit: Maximum number of stories to return (default: 10, max: 50)
    
    Returns:
        Dictionary containing feed information and list of news stories
    """
    # Validate limit parameter
    if limit < 1:
        limit = 1
    elif limit > 50:
        limit = 50
    
    rss_url = "https://www.thoroughbreddailynews.com/feed/"
    
    result = parse_rss_feed(rss_url)
    
    # If there was an error, return it
    if "error" in result:
        return result
    
    # Limit the number of stories returned
    if "stories" in result and len(result["stories"]) > limit:
        result["stories"] = result["stories"][:limit]
        result["total_stories"] = len(result["stories"])
        result["note"] = f"Limited to {limit} stories (use limit parameter to adjust)"
    
    return result

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()