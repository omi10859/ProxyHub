# ProxyHub: A Minimal Django API Gateway

ProxyHub is a simple, extensible API Gateway built with Django and Django REST Framework (DRF). It authenticates requests using API keys, enforces per-key rate limits using Redis, proxies requests to downstream services, and logs all requests for auditing and analytics.

## Features

- **API Key Authentication:** Secure access using unique API keys per client.
- **Rate Limiting:** Configurable per-key rate limiting powered by Redis.
- **Request Proxying:** Forwards all HTTP methods (GET, POST, PUT, DELETE, etc.) with full header/body transparency to downstream services.
- **Request Logging:** Logs all proxied requests with details including API key, downstream service, path, method, response status, and latency.
- **Streaming Responses:** Handles large responses efficiently via Django's `StreamingHttpResponse`.

## FUTURE Improvements

- **Test Cases**
- **Improved Time Log**
- **Api access with authentication to managed services, view logs**

## Quick Start

### 1. Clone the Repository

```sh
git clone https://github.com/your-org/ProxyHub.git
cd ProxyHub
pip install reqruirments.txt



