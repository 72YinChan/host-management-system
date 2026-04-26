import time
import logging

from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger("django")


class RequestElapsedTimeMiddleware(MiddlewareMixin):
    """统计每个请求耗时中间件"""
    def process_request(self, request):
        request.start_time = time.perf_counter()

    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            elapsed_time = time.perf_counter() - request.start_time
            logger.info(f"请求: {request.method} {request.path} | 耗时: {elapsed_time * 1000:.3f}ms")
        return response
