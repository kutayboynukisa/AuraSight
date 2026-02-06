from crawl4ai import AsyncWebCrawler

async def scout_website(url: str) -> str | None:
    """
    Navigates to the target URL and fetches the content in Markdown format.
    Returns None if it fails.
    """
    print(f"🕵️  [AuraSight] Scouting target: {url}...")
    
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url=url)
        
        if result.success:
            return result.markdown
        
        print(f"❌ Failed to scout {url}: {result.error_message}")
        return None