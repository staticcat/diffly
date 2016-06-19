from flask import Flask


def create_app(name, config_obj):
    app = Flask(name)
    if config_obj is not None:
        app.config.from_object(config_obj)

    return app
