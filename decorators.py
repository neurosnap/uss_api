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

def flask_api(template="api.html", title="Some API Title", **api_kwargs):
    """ Primary abstraction to simplify the web browsable API
    It figures out where the request is coming from -- e.g. browser, curl -- and
    determines how to send the response data.

    :param template:  template to be used by the web accessible version of the API call
    :param title: title of API request """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_val = func(*args, **kwargs)
            response = json.dumps(func_val, sort_keys=True, indent=2,
                                    separators=(',', ': '))
            req = "%s %s" % (request.method,
                            request.path.replace(" ", "%20"))

            user_agent = request.headers.get("User-Agent")
            format_as = request.args.get("format")

            if not_browser(user_agent, format_as):
                return jsonify(**func_val)
            else:
                return render_template(template, request=req,
                                        response=response, title=title,
                                        **api_kwargs)
        return wrapper
    return decorator