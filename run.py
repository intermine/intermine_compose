import os
from intermine_compose import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=os.environ.get("FLASK_PORT", "9991"),
        debug=os.environ.get("FLASK_DEBUG", True),
        load_dotenv=os.environ.get("FLASK_LOAD_ENV", True)
    )