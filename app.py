from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
