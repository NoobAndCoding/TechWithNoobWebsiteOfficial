# -- Import a function from the /website/ directory to create the web app --
from website import create_app

# -- Actually initialize the function --
app = create_app()

# -- Run the web app --
if __name__ == "__main__":
    app.run()
