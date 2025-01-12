from flask import Flask, render_template
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
app = Flask(__name__)

# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-cf192832-cac4-4813-a037-6ba18e798dcd"
pnconfig.publish_key = "pub-c-75f67faf-dd39-4f1c-9d61-c252d6b322e8"
pnconfig.uuid = "flight-flask-app-uuid"
pubnub = PubNub(pnconfig)


latest_message = {"status": "No messages yet", "distance": None}


class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        global latest_message
        latest_message = message.message
        print(f"New message: {latest_message}")

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("flight-channel").execute()

@app.route("/")
def home():
    return render_template("index.html", message=latest_message)


@app.route('/land')
def land():
    # Logic for landing (to be implemented)
    return "Landing initiated!"

@app.route('/takeoff')
def takeoff():
    # Logic for takeoff (to be implemented)
    return "Takeoff initiated!"

if __name__ == '__main__':
    app.run(debug=True)
