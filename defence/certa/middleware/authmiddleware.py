from django.urls import reverse
from django.http import HttpResponseRedirect

# class AuthenticationRequiredMiddleware:
#     def process_request(self, request):
#         if not request.user.is_authenticated():
#             return HttpResponseRedirect(reverse('home')) # or http response
#         return None

class AuthenticationRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        print(self)
        print(request)
        print(view_func)
        if request.user.is_authenticated:
            request.role=None
            groups=request.user.groups.all()
            if groups:
                request.role=groups[0].rol
                request.VG=groups[0].VG
                print('middleware',request.role)
        # return HttpResponseRedirect(reverse('home'))
        