from functools import wraps
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwrgs):
        from django.core.handlers.wsgi import WSGIRequest
        request = [a for a in args if isinstance(a, WSGIRequest)][0]
        user = request.__dict__.get('user', None) if request else None 
        if user is None or not user.is_authenticated():
            return HttpResponse(status=403)
        return fn(*args, **kwrgs)
    return wrapper


def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwrgs):
        from django.core.handlers.wsgi import WSGIRequest
        request = [a for a in args if isinstance(a, WSGIRequest)][0]
        user = request.__dict__.get('user', None) if request else None
        if not user.is_manager_of_any_group:
            return HttpResponse(
                loader.render_to_string(
                    '401.html', RequestContext(
                        request, {
                            'error_message': _("You are not allowed to perform this job.")})),
                status=403)
        return fn(*args, **kwrgs)
    return wrapper