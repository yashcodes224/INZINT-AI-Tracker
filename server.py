from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/start-timer', methods=['POST'])
def start_timer():
    data = request.json
    print("API called with data:", data)
    return jsonify({"message": "Timer started successfully"}), 200

if __name__ == "__main__":
    app.run(port=8000)
