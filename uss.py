from __future__ import division, print_function

import json
from functools import wraps

from flask import Flask, render_template, request, \
                    flash, redirect, url_for, jsonify

from ua_parser import user_agent_parser
import us

class Config(object):
    CSRF_ENABLED = False
    DEBUG = True

def create_app():
    app = Flask(__name__)
    # default config
    app.config.from_object(__name__ + '.Config')
    # attempt to import settings from settings file
    try:
        app.config.from_object('local_settings')
    except:
        pass

    def flask_api(title="Some API Title", template="api.html"):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                format_as = request.args.get("format")

                func_val = func(*args, **kwargs)
                response = json.dumps(func_val, sort_keys=True, indent=2, separators=(',', ': '))
                req = "%s %s" % (request.method, request.path.replace(" ", "%20"))
                user_agent = user_agent_parser.Parse(request.headers.get("User-Agent"))

                if (format_as == "json"
                    or user_agent['os']['family'] == "Other"
                    or user_agent['user_agent']['family'] == "Other"):
                        return jsonify(**func_val)
                else:
                    return render_template(template, request=req, response=response, title=title)
            return wrapper
        return decorator

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about/")
    def about():
        return render_template("about.html")

    @app.route("/states/")
    @flask_api("State List")
    def states():
        return { "states": [str(state) for state in us.states.STATES] }

    @app.route("/states/abbr/")
    @flask_api("State Abbreviations List")
    def states_abbreviation():
        return { "states": [str(state.abbr) for state in us.states.STATES] }

    @app.route("/state/")
    def state_list():
        state_list = [str(state) for state in us.states.STATES]
        abbr_list = [str(state.abbr) for state in us.states.STATES]
        return render_template("state_list.html", state_list=state_list, abbr_list=abbr_list)

    @app.route("/state/<path:state>/")
    @flask_api("State Information", "state.html")
    def state(state):
        state_info = us.states.lookup(state)
        if state_info:
            return state_info.__dict__
        else:
            return { "name": "Not found", "error": "No state information found" }

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
