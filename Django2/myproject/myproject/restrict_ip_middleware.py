import ipaddress


class AllowIPMiddleware:
    allowed_networks = [ipaddress.ip_network('')]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        ip_addr = ipaddress.ip_address(ip)
        print(f'Incoming IP: {ip}')
        print(f'X-Forwarded-For: {request.META.get("HTTP_X_FORWARDED_FOR")}')

        allowed = any(ip_addr in net for net in self.allowed_networks)

        if not allowed:
            from django.http import HttpResponseNotFound
            return HttpResponseNotFound()


        response = self.get_response(request)
        return response
