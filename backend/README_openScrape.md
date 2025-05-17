# OpenScrape

A simple, configurable web scraper that can extract data from static websites and output it in OpenAPI format.

## Features

- Scrape data from static websites using CSS selectors
- Support for pagination
- Custom headers for HTTP requests
- Export data in structured JSON format
- Generate OpenAPI schema for the API
- Use as a library or run as a service

## Installation

All dependencies are already included in the project's pyproject.toml file.

## Usage

### As a Library

```python
from openScrape import WebScraper, ScrapingConfig
import json

# Initialize the scraper
scraper = WebScraper()

# Define a scraping configuration
config = ScrapingConfig(
    url="https://example.com",
    selectors={
        "container": ".product-item",  # Container selector (optional)
        "title": ".product-title",     # Field selectors
        "price": ".product-price",
        "image": "img::src"            # Use '::attr' to extract attributes
    },
    max_pages=2,                       # Number of pages to scrape
    pagination={
        "selector": ".pagination .next",  # Selector for the next page link
        "attr": "href"                    # Attribute containing the URL (optional)
    }
)

# Perform the scraping
result = scraper.scrape_website(config)

# Print or process the results
print(json.dumps(result.dict(), indent=2))

# Get OpenAPI schema
schema = scraper.get_openapi_schema()
with open("openapi_schema.json", "w") as f:
    json.dump(schema, f, indent=2)
```

### As a Service

Run the scraper as a FastAPI service:

```bash
python openScrape.py
```

This will start a web server on http://0.0.0.0:8000 with the following endpoints:

- POST `/scrape`: Submit a scraping configuration and get back the scraped data
- GET `/docs`: Interactive API documentation
- GET `/openapi.json`: The OpenAPI schema

### Example

See the `example_scrape.py` file for a complete example that scrapes quotes from quotes.toscrape.com.

```bash
python example_scrape.py
```

## API Reference

### ScrapingConfig

| Field       | Type               | Description                                |
|-------------|--------------------|-------------------------------------------|
| url         | string             | URL of the website to scrape              |
| selectors   | Dict[str, str]     | CSS selectors for extracting data         |
| pagination  | Optional[Dict]     | Pagination configuration                  |
| max_pages   | int                | Maximum number of pages to scrape         |
| headers     | Optional[Dict]     | Custom headers for the request            |

### Selector Syntax

- Basic selectors: Use standard CSS selectors like `.class`, `#id`, etc.
- Attribute extraction: Use `selector::attribute` syntax to extract attributes
- Special selectors:
  - `container`: Special selector that defines item containers (optional)
  - Other keys become field names in the output data

## Best Practices

1. Start with smaller `max_pages` values when testing
2. Include a reasonable user agent in headers
3. Be respectful of website's robots.txt and rate limits
4. For more complex websites, consider using a specialized scraping solution

## License

MIT 