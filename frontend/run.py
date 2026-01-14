from frontend.constant import Constants
from frontend.frontend.app import createApp

# run App
runApp = createApp()

if __name__ == "__main__":
    runApp.run(debug=True, host=Constants.HOST, port=Constants.PORT)
