from openScrape import WebScraper, ScrapingConfig
import json

def example():
    # Initialize the scraper
    scraper = WebScraper()
    
    # Define a scraping configuration for a simple example website
    config = ScrapingConfig(
        url="https://quotes.toscrape.com/",
        selectors={
            # Container for each quote
            "container": ".quote",
            # Text of the quote
            "text": ".text",
            # Author of the quote
            "author": ".author",
            # Tags associated with the quote
            "tags": ".tags .tag"
        },
        max_pages=2,
        pagination={
            "selector": ".next a",
        }
    )
    
    # Perform the scraping
    print("Scraping website...")
    result = scraper.scrape_website(config)
    
    # Print the results
    print(f"Scraped {len(result.data)} items from {result.source_url}")
    print("\nFirst 2 items:")
    for item in result.data[:2]:
        print(f"Quote: {item['text']}")
        print(f"Author: {item['author']}")
        print(f"Tags: {', '.join(item['tags']) if isinstance(item['tags'], list) else item['tags']}")
        print()
    
    # Generate and save the OpenAPI schema
    print("Generating OpenAPI schema...")
    schema = scraper.get_openapi_schema()
    
    with open("openapi_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
    
    print("OpenAPI schema saved to openapi_schema.json")
    
    # Return the data for potential further processing
    return result

if __name__ == "__main__":
    example() 