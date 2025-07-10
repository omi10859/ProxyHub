import requests
import time

from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from .models import Service, ProxyRequestLog
from .authentication import APIKeyRequiredMixin
from .middleware import RateLimitMixin

#  relevant only for a single transport-level connection, removing before next call
HOP_BY_HOP_HEADERS = {
    'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization',
    'te', 'trailers', 'transfer-encoding', 'upgrade', 'host'
}

class ProxyView(RateLimitMixin, APIKeyRequiredMixin, APIView):
    
    def handle_proxy(self, request, service, full_url, start):
        
        upstream_headers = {key: value for key, value in request.headers.items() if key.lower() not in HOP_BY_HOP_HEADERS}

        request_body = request.body
        if request.method.upper() in ['GET', 'HEAD', 'DELETE', 'OPTIONS']:
            # These methods should not have a body. removing the headers and set the body to None.
            upstream_headers.pop('Content-Type', None)
            upstream_headers.pop('Content-Length', None)
            request_body = None
        
        try:
            upstream_response = requests.request(
                method=request.method,
                url=full_url,
                headers=upstream_headers,
                params=request.query_params,
                data=request_body,
                stream=True,
                timeout=30,
                allow_redirects=False
            )
        except requests.RequestException as e:
            return Response({"error": "Request failed", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # streaming the response
        response = StreamingHttpResponse(
            streaming_content=upstream_response.iter_content(chunk_size=8192),
            status=upstream_response.status_code,
            reason=upstream_response.reason,
        )
        for key, value in upstream_response.headers.items():
            if key.lower() not in HOP_BY_HOP_HEADERS:
                response[key] = value
        
        # add log
        duration_ms = (time.time() - start) * 1000
        ProxyRequestLog.objects.create(
            api_key=request.headers.get('X-API-KEY', ''),
            downstream_service=service.base_url,
            path=request.get_full_path(),
            method=request.method,
            response_status=getattr(response, 'status_code', 0),
            duration_ms=duration_ms
        )
        
        return response

    def get(self, request, service_name, subpath=""):
        return self._proxy(request, service_name, subpath)

    def post(self, request, service_name, subpath=""):
        return self._proxy(request, service_name, subpath)

    def put(self, request, service_name, subpath=""):
        return self._proxy(request, service_name, subpath)

    def delete(self, request, service_name, subpath=""):
        return self._proxy(request, service_name, subpath)

    def _proxy(self, request, service_name, subpath):
        start = time.time()

        service = get_object_or_404(Service, name=service_name, is_active=True)
        if subpath:
            full_url = f"{service.base_url.rstrip('/')}/{subpath.lstrip('/')}"
        else:
            full_url = service.base_url

        response = self.handle_proxy(request, service, full_url, start)

        return response
