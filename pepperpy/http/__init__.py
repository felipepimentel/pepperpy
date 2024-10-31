"""HTTP client with advanced features."""
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass, field
import asyncio
import httpx
from loguru import logger
from ..core.config import Config
from ..cache.base import BaseCache, MemoryCache
from ..telemetry import metrics

@dataclass
class HTTPConfig:
    """Configuration for HTTP client."""
    base_url: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    verify_ssl: bool = True
    follow_redirects: bool = True
    cache_enabled: bool = False
    cache_ttl: int = 300  # 5 minutes
    headers: Dict[str, str] = field(default_factory=dict)

class HTTPClient:
    """Enhanced HTTP client with caching and metrics."""
    
    def __init__(
        self,
        config: Optional[HTTPConfig] = None,
        cache: Optional[BaseCache] = None
    ):
        self.config = config or HTTPConfig()
        self.cache = cache if cache and self.config.cache_enabled else None
        self._client = self._create_client()
    
    def _create_client(self) -> httpx.AsyncClient:
        """Create httpx client with configuration."""
        return httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
            follow_redirects=self.config.follow_redirects,
            headers=self.config.headers
        )
    
    async def _make_request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with retries."""
        last_error = None
        
        for attempt in range(self.config.max_retries):
            try:
                response = await self._client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPError as e:
                last_error = e
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (attempt + 1))
                continue
        
        raise last_error
    
    def _get_cache_key(self, method: str, url: str, **kwargs) -> str:
        """Generate cache key for request."""
        from hashlib import sha256
        import json
        
        # Create unique key from request details
        key_data = {
            "method": method,
            "url": url,
            **kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return sha256(key_str.encode()).hexdigest()
    
    async def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with caching and metrics."""
        cache_key = self._get_cache_key(method, url, **kwargs)
        
        # Check cache
        if self.cache:
            if cached := self.cache.get(cache_key):
                logger.debug(f"Cache hit for {method} {url}")
                return cached
        
        # Make request with metrics
        with metrics.timer(f"http.{method.lower()}"):
            response = await self._make_request(method, url, **kwargs)
            data = response.json()
            
            # Cache response
            if self.cache:
                self.cache.set(
                    cache_key,
                    data,
                    ttl=self.config.cache_ttl
                )
            
            return data
    
    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make GET request."""
        return await self.request("GET", url, params=params, **kwargs)
    
    async def post(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make POST request."""
        return await self.request("POST", url, json=json, data=data, **kwargs)
    
    async def put(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return await self.request("PUT", url, json=json, data=data, **kwargs)
    
    async def delete(
        self,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make DELETE request."""
        return await self.request("DELETE", url, **kwargs)
    
    async def close(self) -> None:
        """Close HTTP client."""
        await self._client.aclose()

class APIClient:
    """High-level API client with authentication."""
    
    def __init__(
        self,
        base_url: str,
        auth_token: Optional[str] = None,
        config: Optional[HTTPConfig] = None
    ):
        self.base_url = base_url
        self.auth_token = auth_token
        
        # Configure headers
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        # Create config with base URL and headers
        self.config = config or HTTPConfig()
        self.config.base_url = base_url
        self.config.headers.update(headers)
        
        self.client = HTTPClient(self.config)
    
    async def request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make API request."""
        url = f"{endpoint}"
        return await self.client.request(method, url, **kwargs)
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make GET request to API endpoint."""
        return await self.request("GET", endpoint, params=params, **kwargs)
    
    async def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make POST request to API endpoint."""
        return await self.request(
            "POST",
            endpoint,
            json=json,
            data=data,
            **kwargs
        )
    
    async def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Make PUT request to API endpoint."""
        return await self.request(
            "PUT",
            endpoint,
            json=json,
            data=data,
            **kwargs
        )
    
    async def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make DELETE request to API endpoint."""
        return await self.request("DELETE", endpoint, **kwargs)
    
    async def close(self) -> None:
        """Close API client."""
        await self.client.close()

# Convenience functions
def create_client(
    config: Optional[HTTPConfig] = None,
    cache: Optional[BaseCache] = None
) -> HTTPClient:
    """Create HTTP client instance."""
    return HTTPClient(config, cache)

def create_api_client(
    base_url: str,
    auth_token: Optional[str] = None,
    **kwargs
) -> APIClient:
    """Create API client instance."""
    return APIClient(base_url, auth_token, **kwargs) 