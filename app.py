from __future__ import division, print_function

import json

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

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/about/")
    def about():
        return render_template("about.html")

    @app.route("/states/")
    def states():
        format_as = request.args.get("format")

        states = { "states": [str(state) for state in us.states.STATES] }
        data = json.dumps(states, sort_keys=True, indent=2, separators=(',', ': '))
        response = "GET /states/"

        ua = user_agent_parser.Parse(request.headers.get("User-Agent"))
        if (format_as == "json"
            or ua['os']['family'] == "Other"
            or ua['user_agent']['family'] == "Other"):
                return jsonify(**states)
        else:
            return render_template("api.html", response=response, request=data, title="States List")

    @app.route("/states/abbr/")
    def states_abbreviation():
        format_as = request.args.get("format")

        states = { "states": [str(state.abbr) for state in us.states.STATES] }
        data = json.dumps(states, sort_keys=True, indent=2, separators=(',', ': '))
        response = "GET /states/abbr/"

        ua = user_agent_parser.Parse(request.headers.get("User-Agent"))
        if (format_as == "json"
            or ua['os']['family'] == "Other"
            or ua['user_agent']['family'] == "Other"):
                return jsonify(**states)
        else:
            return render_template("api.html", response=response, request=data, title="States Abbreviations List")

    @app.route("/state/")
    def state_list():
        state_list = [str(state) for state in us.states.STATES]
        return render_template("state_list.html", state_list=state_list)

    @app.route("/state/<path:state>/")
    def state(state):
        format_as = request.args.get("format")

        st = us.states.lookup(state)
        if st:
            st = st.__dict__
        else:
            st = { "name": "Not found", "error": "No state information found" }
        data = json.dumps(st, sort_keys=True, indent=2, separators=(',', ': '))
        response = "GET /state/%s/" % state.replace(" ", "%20")

        ua = user_agent_parser.Parse(request.headers.get("User-Agent"))
        if (format_as == "json"
            or ua['os']['family'] == "Other"
            or ua['user_agent']['family'] == "Other"):
                return jsonify(**st)
        else:
            return render_template("api.html", response=response, request=data, title=st['name'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()