from __future__ import division, print_function

from flask import Flask, render_template, request, \
                    flash, redirect, url_for

import us

class Config(object):
	CSRF_ENABLED = False
    DEBUG = True

def create_app():
    app = Flask(__name__)
    # default config
    app.config.from_object(__name__ + '.ConfigClass')
    # attempt to import settings from settings file
    try:
        app.config.from_object('local_settings')
    except:
        pass

    @app.route("/")
    def index():
        return render_template("index.html")

	@app.route("/state/")
	def state_list():
        states = [str(state) for state in us.states.STATES]
		return render_template("api.html")

	@app.route("/abbr/")
	def state_list_abbreviation():
        states = [str(state.abbr) for state in us.states.STATES]
		return render_template("api.html")

	@app.route("/state/<path:state>/")
	def find_state(state):
        state = us.states.lookup(state).__dict__
		return render_template("api.html")

if __name__ == '__main__':
    app = create_app()
    app.run()