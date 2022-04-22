import webbrowser

from info.gianlucacosta.eos.core.io import reconfigure_output_and_error

from . import APP_URL, DEV_MODE, PORT
from .app import app
from .websockets import socketio

if __name__ == "__main__":
    reconfigure_output_and_error()

    print(f"Welcome to Jardinero! ^__^{' Developer mode is ON!' if DEV_MODE else ''}")

    print()

    print(f"Now listening at: {APP_URL}")

    print()

    print("(press CTRL+C when you want to stop the app)")

    if not DEV_MODE:
        webbrowser.open(APP_URL)

    socketio.run(
        app,
        port=PORT,
        debug=DEV_MODE,
    )
