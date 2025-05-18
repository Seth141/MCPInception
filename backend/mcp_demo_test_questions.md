# YC MCP Server Demo Test Questions

This file contains specific test questions for each MCP tool function in the YC MCP server. Use these questions during your demo to showcase the server's capabilities.

## Basic Batch Retrieval (`yc_batch`)

1. "Could you use the yc_batch tool to show me companies from the Summer 2005 batch?"
2. "Use the yc_batch tool to retrieve information about the Winter 2016 YC batch."
3. "I'd like to see companies from YC's Summer 2015 batch using the yc_batch tool."
4. "Can you use the yc_batch tool to show me the Winter 2020 batch companies?"
5. "Please use the yc_batch tool to retrieve information about the most recent YC batch (Summer 2025)."

## All Batches Retrieval (`yc_all_batches`)

1. "Could you use the yc_all_batches tool to get a list of all YC batches and their companies?"
2. "I'd like to see all YC batches using the yc_all_batches tool."
3. "Use the yc_all_batches tool to retrieve a complete list of YC companies across all batches."

## Industry Filtering (`yc_companies_by_industry`)

1. "Could you use the yc_companies_by_industry tool to find B2B companies?"
2. "I'm interested in Fintech startups. Can you use the yc_companies_by_industry tool to find them?"
3. "Use the yc_companies_by_industry tool to show me Healthcare companies from YC."
4. "Can you find AI companies using the yc_companies_by_industry tool?"
5. "Please use the yc_companies_by_industry tool to identify Consumer companies in YC's portfolio."

## Status Filtering (`yc_companies_by_status`)

1. "Could you use the yc_companies_by_status tool to find Acquired companies?"
2. "I'd like to see Active YC companies. Can you use the yc_companies_by_status tool for this?"
3. "Use the yc_companies_by_status tool to show me Inactive companies from YC."
4. "Can you find Public companies using the yc_companies_by_status tool?"

## Region Filtering (`yc_companies_by_region`)

1. "Could you use the yc_companies_by_region tool to find companies in Europe?"
2. "I'm interested in YC companies from Asia. Can you use the yc_companies_by_region tool to find them?"
3. "Use the yc_companies_by_region tool to show me companies from Latin America."
4. "Can you find Canadian companies using the yc_companies_by_region tool?"
5. "Please use the yc_companies_by_region tool to identify companies in the United States."

## Text Search (`yc_search_companies`)

1. "Could you use the yc_search_companies tool to find companies related to 'blockchain'?"
2. "I'm interested in 'climate' technology. Can you use the yc_search_companies tool to find relevant companies?"
3. "Use the yc_search_companies tool to search for companies related to 'education'."
4. "Can you find companies related to 'robotics' using the yc_search_companies tool?"
5. "Please use the yc_search_companies tool to search for companies with 'AI' in their description or tags."

## Founder Name Search (`yc_companies_by_founder_name`)

1. "Could you use the yc_companies_by_founder_name tool to find companies founded by someone named 'Paul'?"
2. "I'm interested in companies founded by 'Sam'. Can you use the yc_companies_by_founder_name tool to find them?"
3. "Use the yc_companies_by_founder_name tool to show me companies with founders named 'Jessica'."
4. "Can you find companies with founders named 'Michael' using the yc_companies_by_founder_name tool?"
5. "Please use the yc_companies_by_founder_name tool to identify companies founded by someone named 'Alex'."

## Advanced Multi-Filter Search (`yc_advanced_search`)

1. "Could you use the yc_advanced_search tool to find active B2B companies in the United States?"
2. "I'm looking for acquired fintech companies from 2015-2020 batches. Can you use the yc_advanced_search tool for this?"
3. "Use the yc_advanced_search tool to find healthcare companies in Europe that are still active."
4. "Can you find B2B companies with more than 50 team members using the yc_advanced_search tool?"
5. "Please use the yc_advanced_search tool to search for AI companies in the Winter 2020 batch."

## Resource Endpoints (via `read_resource`)

1. "Could you read the resource at mcp://yc/summer-2015.json?"
2. "I'd like to see the contents of the mcp://yc/winter-2016.json resource."
3. "Can you access the resource at mcp://yc/summer-2005.json?"
4. "Please read the mcp://yc/winter-2020.json resource."

## Combined Queries (Multiple Tools)

1. "First use the yc_batch tool to get the Summer 2015 batch, then use the yc_companies_by_industry tool to filter for B2B companies from that batch."
2. "Could you use the yc_companies_by_region tool to find companies in Europe, and then use the yc_companies_by_status tool to see which ones are still active?"
3. "Use the yc_search_companies tool to find AI companies, then use the yc_advanced_search tool to filter for ones with more than 20 team members."

## Demo Workflow Example

Here's a suggested workflow for your demo:

1. Start with basic batch retrieval: "Show me the Summer 2015 batch using the yc_batch tool."
2. Move to industry filtering: "Now use the yc_companies_by_industry tool to find B2B companies."
3. Try region filtering: "Can you use the yc_companies_by_region tool to find companies in Europe?"
4. Demonstrate text search: "Let's use the yc_search_companies tool to find companies related to 'AI'."
5. Show founder search: "Use the yc_companies_by_founder_name tool to find companies founded by someone named 'Paul'."
6. Finish with advanced search: "Finally, use the yc_advanced_search tool to find active B2B companies in the United States with more than 50 team members."

This progression will showcase the full range of capabilities in your MCP server, from simple queries to complex multi-filter searches.
