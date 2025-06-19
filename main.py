import requests
import xml.etree.ElementTree as ET
from html import unescape
import re

def clean_html(text):
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

def fetch_and_parse_rss(url):
    """Fetch RSS feed and parse the XML content."""
    try:
        # Fetch the RSS feed
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the XML
        root = ET.fromstring(response.content)
        
        # Find the channel element
        channel = root.find('channel')
        if channel is None:
            print("Error: Could not find channel element in RSS feed")
            return
        
        print(f"Feed Title: {channel.find('title').text if channel.find('title') is not None else 'N/A'}")
        print(f"Feed Description: {channel.find('description').text if channel.find('description') is not None else 'N/A'}")
        print("=" * 80)
        print()
        
        # Find all item elements
        items = channel.findall('item')
        
        if not items:
            print("No stories found in the RSS feed.")
            return
        
        print(f"Found {len(items)} stories:\n")
        
        # Process each story
        for i, item in enumerate(items, 1):
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            pub_date = item.find('pubDate')
            
            print(f"Story #{i}")
            print("-" * 40)
            
            # Title
            title_text = title.text if title is not None else "No title available"
            print(f"Title: {clean_html(title_text)}")
            
            # Publication date
            if pub_date is not None:
                print(f"Published: {pub_date.text}")
            
            # Link
            link_text = link.text if link is not None else "No link available"
            print(f"Link: {link_text}")
            
            # Content/Description
            if description is not None:
                content = clean_html(description.text)
                # Truncate very long content for readability
                if len(content) > 500:
                    content = content[:500] + "..."
                print(f"Content: {content}")
            else:
                print("Content: No content available")
            
            print()
            print("=" * 80)
            print()
    
    except requests.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    """Main function to run the RSS parser."""
    rss_url = "https://www.thoroughbreddailynews.com/feed/"
    
    print("Thoroughbred Daily News RSS Parser")
    print("=" * 40)
    print(f"Fetching feed from: {rss_url}")
    print()
    
    fetch_and_parse_rss(rss_url)

if __name__ == "__main__":
    main()