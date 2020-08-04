import os
from intermine_compose import app
from intermine_compose.config import Config


app = app.create_app(Config.PROD)

if __name__ == "__main__":
    app.run(
        host=app.config.get("FLASK_HOST"),
        port=app.config.get("FLASK_PORT"),
        debug=app.config.get("FLASK_DEBUG"),
    )
