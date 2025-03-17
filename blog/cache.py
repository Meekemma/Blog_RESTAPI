from django.core.cache import cache

def get_cached_data(cache_key):
    """Retrieve cached data if available."""
    return cache.get(cache_key)

def set_cached_data(cache_key, data, timeout=600):
    """Store JSON-serializable data in cache for a specified timeout."""
    cache.set(cache_key, data, timeout)  # Only store JSON (not Response object)

def clear_cache():
    """Clears all cached data."""
    cache.clear()
