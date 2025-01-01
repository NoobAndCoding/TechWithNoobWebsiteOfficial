# -- Initialize the imports --
import os
from app import app

# -- Run the WSGI server --
if __name__ == "__main__":
    # -- Define the server port --
    port = int(os.environ.get("PORT", 10000))
    # -- Initialize the WSGI server --
    app.run(host = "0.0.0.0", port = port)