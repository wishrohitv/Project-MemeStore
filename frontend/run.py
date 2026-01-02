from frontend.controllers.app import createApp
from frontend.constant import Constants


# run App
runApp = createApp()

if __name__ == "__main__":
    runApp.run(debug=True, host=Constants.HOST, port=Constants.PORT)
