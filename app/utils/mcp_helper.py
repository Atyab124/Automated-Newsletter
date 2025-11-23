"""
Helper module for Playwright MCP integration

This module provides a way to use Playwright MCP tools when available.
In Cursor, MCP tools are available through the function interface.
"""
from typing import Optional, Dict, List
import sys


class MCPHelper:
    """
    Helper class to use Playwright MCP tools
    
    Note: In Cursor, MCP tools are available as functions.
    This class provides a wrapper interface.
    """
    
    def __init__(self, mcp_tools=None):
        """
        Initialize with optional MCP tools
        
        Args:
            mcp_tools: Dictionary of MCP tool functions (optional)
        """
        self.mcp_tools = mcp_tools or {}
        self.has_mcp = bool(mcp_tools)
    
    def navigate(self, url: str) -> bool:
        """Navigate to URL"""
        if not self.has_mcp:
            return False
        
        try:
            # In Cursor, this would call: mcp_Playwright_browser_navigate(url=url)
            if 'navigate' in self.mcp_tools:
                self.mcp_tools['navigate'](url=url)
                return True
        except Exception as e:
            print(f"MCP navigate error: {e}")
        return False
    
    def snapshot(self) -> Optional[Dict]:
        """Get page snapshot"""
        if not self.has_mcp:
            return None
        
        try:
            if 'snapshot' in self.mcp_tools:
                return self.mcp_tools['snapshot']()
        except Exception as e:
            print(f"MCP snapshot error: {e}")
        return None
    
    def extract_links_from_snapshot(self, snapshot: Dict) -> List[Dict]:
        """
        Extract links and text from accessibility snapshot
        
        This is a helper to parse the snapshot structure.
        The actual structure depends on the page.
        """
        links = []
        
        if not snapshot:
            return links
        
        # Parse snapshot structure
        # This is a simplified parser - actual implementation would need
        # to handle the specific structure of accessibility snapshots
        def traverse(node, parent_text=""):
            if isinstance(node, dict):
                node_type = node.get('type', '')
                text = node.get('text', '')
                href = node.get('href', '')
                
                if href:
                    links.append({
                        'text': text or parent_text,
                        'url': href
                    })
                
                # Recursively process children
                for key, value in node.items():
                    if key not in ['type', 'text', 'href']:
                        traverse(value, text or parent_text)
            elif isinstance(node, list):
                for item in node:
                    traverse(item, parent_text)
        
        traverse(snapshot)
        return links

