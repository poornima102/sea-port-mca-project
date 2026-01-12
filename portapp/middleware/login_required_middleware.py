from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be logged in to access certain pages.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [
            '/', '/user_login', '/user_login/', '/register_user', '/register_user/',
            '/register_company', '/register_company/', '/register_contract', '/register_contract/',
            '/logout/',
        ]

    def __call__(self, request):
        # Require session for all pages except those in exempt_paths
        if not (
            request.session.get('user_id') or
            request.session.get('admin_id') or
            request.session.get('company_id') or
            request.session.get('contract_id')
        ) and request.path not in self.exempt_paths:
            return redirect('user_login')
        response = self.get_response(request)
        # Prevent browser caching of protected pages
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response