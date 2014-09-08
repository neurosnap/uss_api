from __future__ import division, print_function

from flask import Flask, render_template
import us

from decorators import render_api, api, FlaskAPI

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

    @app.route("/states/<int:id>/", methods=["GET", "POST"])
    @app.route("/states/")
    @api
    class States(FlaskAPI):

        def get(self, id=None):
            states = [str(state) for state in us.states.STATES]
            return render_api({ "states": states },
                                title="State List")
        def post(self, id):
            return render_api({ "post": "I did a post bitch", "id": id }, title="States List")

    @app.route("/states/abbr/")
    def states_abbreviation():
        states = [str(state.abbr) for state in us.states.STATES]
        return render_api({ "states": states },
                            title="State Abbreviations List")

    @app.route("/state/")
    def state_list():
        state_list = [str(state) for state in us.states.STATES]
        abbr_list = [str(state.abbr) for state in us.states.STATES]
        return render_template("state_list.html", state_list=state_list,
                                abbr_list=abbr_list)

    @app.route("/state/<path:state>/")
    def state(state):
        state_info = us.states.lookup(state)
        if state_info:
            res = state_info.__dict__
        else:
            res = {
                "name": "Not found",
                "error": "No state information found"
            }
        return render_api(res, title="State Information")

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
