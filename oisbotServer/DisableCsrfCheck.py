from django.utils.deprecation import MiddlewareMixin

class DisableCsrfCheck(MiddlewareMixin):

    def processRequest(self, req):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(req, attr, False):
            setattr(req, attr, True)