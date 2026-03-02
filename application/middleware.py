from .models import VisitorLog

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith('/admin/'):
            def get_client_ip(request):
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                return ip

            ip = get_client_ip(request)
            VisitorLog.objects.create(
                ip_address=ip,
                path=request.path,
                method=request.method,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255]
            )
        
        return response
