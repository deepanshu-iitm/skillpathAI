import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_resources(query, num_results=5):
    """
    Search Google dynamically for a query using Serper API.
    Returns a list of dictionaries with 'title', 'url', and 'snippet'.
    """
    if not SERPER_API_KEY:
        return []
    
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "num": num_results
    }
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json()
        
        resources = []
        for item in results.get("organic", []):
            resources.append({
                "type": "Web",
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet")
            })
        return resources
    except Exception as e:
        print(f"Serper API error: {e}")
        return []

def search_youtube_videos(topic, num_results=3):
    """Search for YouTube videos related to the topic"""
    query = f"{topic} tutorial youtube"
    return search_resources(query, num_results)

def search_articles_blogs(topic, num_results=3):
    """Search for articles and blog posts related to the topic"""
    query = f"{topic} guide article blog tutorial"
    return search_resources(query, num_results)

def get_comprehensive_resources(topic, day_topic):
    """Get a comprehensive set of resources for a learning topic"""
    all_resources = []
    
    # YouTube videos
    youtube_query = f"{topic} {day_topic} tutorial video"
    youtube_results = search_resources(youtube_query, 2)
    for result in youtube_results:
        if "youtube.com" in result["url"]:
            result["type"] = "YouTube"
            all_resources.append(result)
    
    # Articles and blogs
    article_query = f"{topic} {day_topic} guide tutorial"
    article_results = search_resources(article_query, 3)
    for result in article_results:
        if "youtube.com" not in result["url"]:
            result["type"] = "Article"
            all_resources.append(result)
    
    # Documentation/official resources
    docs_query = f"{topic} {day_topic} documentation official"
    docs_results = search_resources(docs_query, 2)
    for result in docs_results:
        if any(domain in result["url"] for domain in ["docs.", "documentation", "official"]):
            result["type"] = "Documentation"
        else:
            result["type"] = "Resource"
        all_resources.append(result)
    
    return all_resources[:8]  # Limit to 8 total resources

def get_limited_resources_for_overview(topic, day_topic):
    """Get limited resources for the overview page: 1 YouTube, 1 Article, 1 Blog"""
    limited_resources = []
    
    # Get 1 YouTube video
    youtube_query = f"{topic} {day_topic} tutorial video"
    youtube_results = search_resources(youtube_query, 3)
    for result in youtube_results:
        if "youtube.com" in result["url"]:
            result["type"] = "YouTube"
            limited_resources.append(result)
            break  # Only take the first YouTube result
    
    # Get 1 Article
    article_query = f"{topic} {day_topic} guide tutorial"
    article_results = search_resources(article_query, 5)
    for result in article_results:
        if "youtube.com" not in result["url"] and any(domain in result["url"] for domain in ["medium.com", "dev.to", "towardsdatascience.com", "blog", "article"]):
            result["type"] = "Article"
            limited_resources.append(result)
            break  # Only take the first article
    
    # Get 1 Blog post (different from article)
    blog_query = f"{topic} {day_topic} blog post tutorial"
    blog_results = search_resources(blog_query, 5)
    for result in blog_results:
        if "youtube.com" not in result["url"] and result["url"] not in [r["url"] for r in limited_resources]:
            result["type"] = "Blog"
            limited_resources.append(result)
            break  # Only take the first unique blog
    
    # If we don't have 3 resources, fill with general web results
    if len(limited_resources) < 3:
        general_results = search_resources(f"{topic} {day_topic}", 5)
        for result in general_results:
            if result["url"] not in [r["url"] for r in limited_resources]:
                result["type"] = "Resource"
                limited_resources.append(result)
                if len(limited_resources) >= 3:
                    break
    
    return limited_resources[:3]  # Ensure exactly 3 resources
