""" Decorators used by USS API """
import json
from functools import wraps

from flask import request, render_template, jsonify
from ua_parser import user_agent_parser

def not_browser(user_agent, format_as):
    ua = user_agent_parser.Parse(user_agent)
    if (ua['os']['family'] == "Other"
        or ua['user_agent']['family'] == "Other"
        or format_as == "json"):
            return True

    return False


class FlaskAPI(object):
    def __init__(self, *args, **kwargs):
        pass #super(FlaskAPI, self).__init__(*args, **kwargs)

def api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_val = func(*args, **kwargs)
        if request.method == "GET":
            return func_val.get(*args, **kwargs)
        if request.method == "POST":
            return func_val.post(*args, **kwargs)
        if request.method == "PUT":
            return func_val.put(*args, **kwargs)
        if request.method == "UPDATE":
            return func_val.update(*args, **kwargs)
        if request.method == "DELETE":
            return func_val.delete(*args, **kwargs)
    return wrapper

def render_api(res_object, template="api.html", **kwargs):
    """ Primary abstraction to simplify the web browsable API
    It figures out where the request is coming from -- e.g. browser, curl -- and
    determines how to send the response data.

    :param res_object: response dictionary object to be JSON serialized
    :param template:  template to be used by the web accessible version of the API call """
    response = json.dumps(res_object, sort_keys=True, indent=2,
                                    separators=(',', ': '))
    req = "%s %s" % (request.method,
                    request.path.replace(" ", "%20"))

    user_agent = request.headers.get("User-Agent")
    format_as = request.args.get("format")

    if not_browser(user_agent, format_as):
        return jsonify(**res_object)
    else:
        return render_template(template, request=req, response=response,
                                **kwargs)