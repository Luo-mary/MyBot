from flask import Flask, request, jsonify
import logging

# Initialize Flask app
app = Flask(__name__)

# Setup logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@app.route('/')
def home():
    """Default route to test if the Flask app is running."""
    return "Flask app is running! Use /interactions for Discord events."

@app.route('/interactions', methods=['POST', 'GET'])
def interactions():
    """Handle Discord interactions."""
    try:
        # Handle GET requests for debugging
        if request.method == 'GET':
            return "This is the /interactions endpoint. Use POST to interact with it."

        # Handle POST requests for Discord interactions
        data = request.json
        logging.info(f"Received interaction: {data}")

        # Ping event: Respond to Discord's validation request
        if data.get("type") == 1:
            return jsonify({"type": 1})  # Acknowledge Ping

        # Application command (type 2)
        elif data.get("type") == 2:
            command_name = data["data"]["name"]

            # Handle the `/describe` command
            if command_name == "describe":
                image_url = data["data"]["options"][0]["value"]
                logging.info(f"Processing /describe command for URL: {image_url}")
                return jsonify({
                    "type": 4,  # Immediate channel message response
                    "data": {
                        "content": f"Describing image: {image_url}"
                    }
                })

            # Handle unknown commands
            else:
                logging.warning(f"Unknown command: {command_name}")
                return jsonify({
                    "type": 4,
                    "data": {
                        "content": f"Unknown command: {command_name}"
                    }
                })

        # Unknown interaction type
        logging.error("Unknown interaction type received.")
        return jsonify({"error": "Unknown interaction type"}), 400

    except Exception as e:
        # Log unexpected errors
        logging.error(f"Error handling interaction: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Host and port configuration
    HOST = "0.0.0.0"  # Accessible from any network interface
    PORT = 5003       # Default port for the Flask app
    logging.info(f"Starting Flask server on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT)
