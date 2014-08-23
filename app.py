from __future__ import division, print_function

from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

import us

app = FlaskAPI(__name__)

app.config['DEFAULT_RENDERERS'] = [
    'flask.ext.api.renderers.JSONRenderer',
    'flask.ext.api.renderers.BrowsableAPIRenderer',
]

@app.route("/")
def state_list():
	return [str(state) for state in us.states.STATES]

@app.route("/abbr")
def state_list_abbreviation():
	return [str(state.abbr) for state in us.states.STATES]

@app.route("/state/<path:state>")
def find_state(state):
	return us.states.lookup(state).__dict__

if __name__ == '__main__':
	app.run(debug=True)