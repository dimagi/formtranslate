from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from formtranslate import api
import json


def home(request):
    return render_to_response("formtranslate/home.html", RequestContext(request))


def _wrapped_api_call(request, api_func):
    file = request.POST["xform"]
    ret = {"success": False, "errstring": "", "outstring": ""}
    if not file:
        ret.update(**{"success": False, "errstring": "No form present!"})
    else:
        file = file.encode('utf-8')
        result = api_func(file, get_raw=True)
        ret['outstring'] = result.stdout
        ret['errstring'] = result.stderr
    return HttpResponse(json.dumps(ret), content_type="text/json")


@require_POST
def validate(request):
    """
    Validate a form
    """
    return _wrapped_api_call(request, api.validate)
    
    
@require_POST
def readable(request):
    """
    Get a readable form
    """
    return _wrapped_api_call(request, api.readable_form)
    
@require_POST    
def csv(request):
    """
    Get the csv translation file from an xform
    """
    return _wrapped_api_call(request, api.csv_dump)
    
    
@require_POST
def xsd(request):
    """
    Translates an xform into an xsd file
    """
    return _wrapped_api_call(request, api.get_xsd_schema)
