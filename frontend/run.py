from frontend.app.app import createApp
from frontend.constant import Constants

# run App
app = createApp()

if __name__ == "__main__":
    app.run(debug=True, host=Constants.HOST, port=Constants.PORT)
