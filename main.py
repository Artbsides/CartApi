import os
import sentry_sdk

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_httpauth import HTTPBasicAuth

from sentry_sdk import capture_exception
from sentry_sdk.integrations.flask import FlaskIntegration

from prometheus_flask_exporter import RESTfulPrometheusMetrics

from debugger import debugger
from app.routes import load_routes


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    debug=os.getenv("FLASK_DEBUG").lower() in ["1", "true"],
    release=f'{os.getenv("APP_RELEASE")}-{os.getenv("APP_ENVIRONMENT")}',
    environment=os.getenv("APP_ENVIRONMENT"),
    traces_sample_rate=1.0,
    integrations=[
        FlaskIntegration(),
    ]
)


app = Flask(__name__)

app.config["MONGODB_HOST"] = f'{os.getenv("MONGODB_URL")}/{os.getenv("MONGODB_NAME")}'
app.config["PROPAGATE_EXCEPTIONS"] = True

restful_api = Api(app,
    default_mediatype="application/json")


if os.getenv("FLASK_DEBUGGER").lower() in ["1", "true"]:
    debugger(os.getenv("FLASK_DEBUGGER_PORT"))

CORS(app, resources={r"/*": {"origins": "*"}})
MongoEngine(app)

metrics_auth = \
    HTTPBasicAuth()

RESTfulPrometheusMetrics(app, restful_api, path="/metrics", metrics_decorator=metrics_auth.login_required)


@metrics_auth.verify_password
def verify_credentials(username, password):
    return (username, password) == (os.getenv("METRICS_USER"), os.getenv("METRICS_PASSWORD"))

@app.errorhandler(404)
def page_not_found(e):
    return {"error": str(e)}, 400

@app.errorhandler(Exception)
def exceptions(e):
    capture_exception(e)

    return {"error": str(e)}, getattr(e, "code", 500)


load_routes(restful_api)


if __name__ == "__main__":
    app.run(host=os.getenv("FLASK_RUN_HOST"), port=os.getenv("FLASK_RUN_PORT"))
