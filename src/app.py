from flask import Flask, request, jsonify
from handler import get_gemini_response

import socket
socket.setdefaulttimeout(900) 


app = Flask(__name__)

def create_response(text):
    return jsonify({
        'fulfillmentMessages': [{
            'text': {
                'text': [text]
            }
        }],
        'source': 'webhook'
    })

@app.route("/")
def handle_home():
    return "ok", 200

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    try:
        data = request.get_json(silent=True, force=True)
        print(data)

        intent_name = data['queryResult']['intent']['displayName']
        if intent_name == "Default Fallback Intent":
            query_text = data['queryResult']['queryText']
            result = get_gemini_response(query_text)
            print(result)

            if 'status' in result and result['status'] == 1:
                return create_response(result.get('response', ''))
            else:
                raise Exception('Gemini Pro did not return a valid response')
        else:
            # Intent name doesn't match, return empty response
            return jsonify({}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return create_response(f"An error occurred: {e}"), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
