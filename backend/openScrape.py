import requests
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScrapingConfig(BaseModel):
    """Configuration for website scraping"""
    url: str = Field(..., description="URL of the website to scrape")
    selectors: Dict[str, str] = Field(..., description="CSS selectors for extracting data")
    pagination: Optional[Dict[str, str]] = Field(None, description="Pagination configuration if needed")
    max_pages: int = Field(1, description="Maximum number of pages to scrape")
    headers: Optional[Dict[str, str]] = Field(None, description="Custom headers for the request")

class ScrapedData(BaseModel):
    """Model for the scraped data"""
    source_url: str
    timestamp: str
    data: List[Dict[str, Any]]

class WebScraper:
    def __init__(self):
        self.app = FastAPI(title="WebScraper API", description="API for scraping static websites")
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up the API routes"""
        @self.app.post("/scrape", response_model=ScrapedData)
        async def scrape(config: ScrapingConfig):
            return self.scrape_website(config)
        
        @self.app.get("/scraper")
        async def simple_scraper(url: str = Query(..., description="URL to scrape"),
                               serverName: Optional[str] = Query(None, description="Optional server name")):
            """Simple endpoint that accepts a URL and returns scraped data"""
            from datetime import datetime
            
            try:
                logger.info(f"Scraping URL: {url}")
                
                # Use a basic configuration that extracts common elements
                config = ScrapingConfig(
                    url=url,
                    selectors={
                        "title": "title",
                        "headings": "h1, h2, h3",
                        "paragraphs": "p",
                        "links": "a::href",
                        "images": "img::src"
                    },
                    max_pages=1
                )
                
                result = self.scrape_website(config)
                
                # Add the server name if provided
                response = {
                    "source_url": url,
                    "timestamp": datetime.now().isoformat(),
                    "data": result.data
                }
                
                if serverName:
                    response["server_name"] = serverName
                
                return response
                
            except Exception as e:
                logger.error(f"Error scraping URL {url}: {str(e)}")
                return {"error": str(e)}
    
    def scrape_website(self, config: ScrapingConfig) -> ScrapedData:
        """Scrape a website based on the provided configuration"""
        from datetime import datetime
        
        all_data = []
        current_url = config.url
        
        try:
            for page in range(config.max_pages):
                logger.info(f"Scraping page {page+1}: {current_url}")
                
                # Make the request
                headers = config.headers or {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                response = requests.get(current_url, headers=headers)
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract data based on selectors
                page_data = self._extract_data(soup, config.selectors)
                all_data.extend(page_data)
                
                # Handle pagination if configured and we haven't reached max_pages
                if config.pagination and page < config.max_pages - 1:
                    next_link = soup.select_one(config.pagination.get("selector", ""))
                    if next_link:
                        if "attr" in config.pagination:
                            next_url = next_link.get(config.pagination["attr"])
                        else:
                            next_url = next_link.get("href")
                            
                        # Handle relative URLs
                        if next_url and not (next_url.startswith("http://") or next_url.startswith("https://")):
                            from urllib.parse import urljoin
                            next_url = urljoin(current_url, next_url)
                        
                        if next_url:
                            current_url = next_url
                        else:
                            break
                    else:
                        break
                else:
                    break
                    
            return ScrapedData(
                source_url=config.url,
                timestamp=datetime.now().isoformat(),
                data=all_data
            )
            
        except Exception as e:
            logger.error(f"Error scraping website: {str(e)}")
            raise
    
    def _extract_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract data from the soup based on the selectors"""
        results = []
        
        # Find the container elements if specified
        container_selector = selectors.pop("container", None)
        containers = soup.select(container_selector) if container_selector else [soup]
        
        for container in containers:
            item_data = {}
            
            for field, selector in selectors.items():
                # Check if we need to extract an attribute
                attr = None
                if "::" in selector:
                    selector, attr = selector.split("::", 1)
                
                elements = container.select(selector)
                
                if len(elements) == 1:
                    element = elements[0]
                    if attr:
                        item_data[field] = element.get(attr, "")
                    else:
                        item_data[field] = element.get_text(strip=True)
                elif len(elements) > 1:
                    if attr:
                        item_data[field] = [element.get(attr, "") for element in elements]
                    else:
                        item_data[field] = [element.get_text(strip=True) for element in elements]
                else:
                    item_data[field] = None
            
            if item_data:
                results.append(item_data)
        
        return results
    
    def get_openapi_schema(self) -> Dict[str, Any]:
        """Generate and return the OpenAPI schema for the API"""
        return get_openapi(
            title=self.app.title,
            version="1.0.0",
            description=self.app.description,
            routes=self.app.routes,
        )

def main():
    """Start the WebScraper service"""
    import uvicorn
    
    scraper = WebScraper()
    
    # Run the service
    uvicorn.run(scraper.app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
