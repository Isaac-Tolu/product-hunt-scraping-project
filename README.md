# Product Hunt Web Scraping

## Objective
Scrape and extract data of products launched on Product Hunt.

The goal is to create a data pipeline that extracts the data at the end of each day and sends it to a database for further processing

## Tools
- Requests
- Beautiful Soup

### On the Limitations of Beautiful Soup
Beautiful Soup is powerful for parsing scraped HTML, but not useful for scraping JS-rich pages. This is where tools like Selenium has to come in. Product Hunt website uses lazy loading. Selenium would help in scraping these data reliably.
