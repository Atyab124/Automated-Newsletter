"""
Research paper scraper using arXiv and Semantic Scholar APIs
"""
import requests
from typing import List, Dict
from .base_scraper import BaseScraper
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import ARXIV_MAX_RESULTS, SEMANTIC_SCHOLAR_MAX_RESULTS


class ResearchScraper(BaseScraper):
    """Scrapes research papers from arXiv and Semantic Scholar"""
    
    def scrape(self, topic: str) -> List[Dict]:
        """
        Scrape research papers for a topic from arXiv and Semantic Scholar
        """
        results = []
        
        # Scrape from arXiv
        arxiv_results = self._scrape_arxiv(topic)
        results.extend(arxiv_results)
        
        # Scrape from Semantic Scholar
        semantic_results = self._scrape_semantic_scholar(topic)
        results.extend(semantic_results)
        
        return results[:self.max_results]
    
    def _scrape_arxiv(self, topic: str) -> List[Dict]:
        """Scrape from arXiv API"""
        results = []
        try:
            # arXiv API endpoint
            url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": f"all:{topic}",
                "start": 0,
                "max_results": ARXIV_MAX_RESULTS,
                "sortBy": "submittedDate",
                "sortOrder": "descending"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            # Namespace for arXiv XML
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                link_elem = entry.find('atom:id', ns)
                
                if title_elem is not None and link_elem is not None:
                    title = title_elem.text.strip() if title_elem.text else ""
                    abstract = summary_elem.text.strip() if summary_elem is not None and summary_elem.text else ""
                    paper_url = link_elem.text if link_elem.text else ""
                    
                    results.append(self.format_result(
                        source="arXiv",
                        headline=title,
                        url=paper_url,
                        abstract=abstract
                    ))
        
        except Exception as e:
            print(f"Error scraping arXiv: {e}")
        
        return results
    
    def _scrape_semantic_scholar(self, topic: str) -> List[Dict]:
        """Scrape from Semantic Scholar API"""
        results = []
        try:
            # Semantic Scholar API endpoint
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": topic,
                "limit": SEMANTIC_SCHOLAR_MAX_RESULTS,
                "sort": "relevance"
            }
            headers = {
                "Accept": "application/json"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                for paper in data['data']:
                    title = paper.get('title', '')
                    abstract = paper.get('abstract', '')
                    paper_id = paper.get('paperId', '')
                    paper_url = f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else ""
                    
                    results.append(self.format_result(
                        source="Semantic Scholar",
                        headline=title,
                        url=paper_url,
                        abstract=abstract
                    ))
        
        except Exception as e:
            print(f"Error scraping Semantic Scholar: {e}")
        
        return results

