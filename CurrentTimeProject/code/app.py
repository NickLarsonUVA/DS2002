from flask import Flask, jsonify, request
from datetime import datetime
import pytz

app = Flask(__name__)

API_TOKEN = "supersecrettoken123"

# Capital to timezone map
capital_timezones = {
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Washington": "America/New_York",
    "Canberra": "Australia/Sydney",
    "Ottawa": "America/Toronto",
    "New Delhi": "Asia/Kolkata",
    "Brasília": "America/Sao_Paulo"
}

def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    decorator.__name__ = f.__name__
    return decorator

@app.route('/api/time/<capital>', methods=['GET'])
@token_required
def get_time(capital):
    if capital not in capital_timezones:
        return jsonify({"error": f"'{capital}' is not a recognized capital city."}), 404

    tz = pytz.timezone(capital_timezones[capital])
    now = datetime.now(tz)
    offset = now.strftime('%z')  #Format help

    #Inserts a colon into the offset for easier read
    offset_formatted = f"{offset[:3]}:{offset[3:]}" if len(offset) == 5 else offset

    return jsonify({
        "capital": capital,
        "local_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "utc_offset": offset_formatted
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
