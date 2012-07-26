# Create your views here.
import prefinery_lib as lib
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings

if not hasattr(settings, "PREFINERY_CALLBACK"):
    raise Exception("PREFINERY_CALLBACK must be defined in settings")

def signup(request):
    email = request.GET['email']
    code = request.GET['code']
    
    tester_id = lib.get_tester_id_by_email(email)
    tester = lib.verify_code(tester_id, code)
    if tester is not None:
        return settings.PREFINERY_CALLBACK(request, tester)
    else:
        return HttpResponseForbidden('Code invalid')