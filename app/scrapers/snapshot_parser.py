"""
Helper module to parse Playwright accessibility snapshots
"""
from typing import List, Dict, Any, Optional


def extract_links_from_snapshot(snapshot: Any) -> List[Dict[str, str]]:
    """
    Extract links and associated text from Playwright accessibility snapshot
    
    Args:
        snapshot: The accessibility snapshot from Playwright MCP
    
    Returns:
        List of dicts with 'text' and 'url' keys
    """
    links = []
    
    if not snapshot:
        return links
    
    def traverse(node: Any, parent_text: str = ""):
        """Recursively traverse the snapshot tree"""
        if isinstance(node, dict):
            # Check if this node is a link
            role = node.get('role', '')
            name = node.get('name', '')
            url = None
            
            # Look for link information
            if 'value' in node and isinstance(node['value'], str) and node['value'].startswith('http'):
                url = node['value']
            elif 'url' in node:
                url = node['url']
            elif 'href' in node:
                url = node['href']
            
            # Get text content
            text = name or parent_text
            
            # If we found a link, add it
            if url and text:
                links.append({
                    'text': text.strip(),
                    'url': url.strip()
                })
            
            # Recursively process children
            for key, value in node.items():
                if key not in ['role', 'name', 'value', 'url', 'href']:
                    traverse(value, text or parent_text)
        
        elif isinstance(node, list):
            for item in node:
                traverse(item, parent_text)
    
    traverse(snapshot)
    return links


def extract_headlines_from_snapshot(snapshot: Any, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Extract headline-like text from snapshot (for news articles)
    
    Args:
        snapshot: The accessibility snapshot
        max_results: Maximum number of results to return
    
    Returns:
        List of dicts with 'text' and 'url' keys
    """
    links = extract_links_from_snapshot(snapshot)
    
    # Filter and prioritize headlines
    # Look for links that might be headlines (usually in article or heading contexts)
    headlines = []
    
    for link in links[:max_results * 2]:  # Get more to filter
        text = link.get('text', '').strip()
        url = link.get('url', '').strip()
        
        # Filter out navigation, footer, and other non-content links
        if (text and url and 
            len(text) > 10 and  # Headlines are usually longer
            not any(skip in url.lower() for skip in ['/search', '/login', '/signup', '/privacy', '/terms', '#']) and
            not any(skip in text.lower() for skip in ['skip', 'menu', 'navigation', 'cookie', 'privacy'])):
            headlines.append({
                'text': text,
                'url': url
            })
    
    return headlines[:max_results]

