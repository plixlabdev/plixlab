import os
import threading
import time
import webbrowser  
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.serving import make_server
import json

UPLOAD_FOLDER = os.path.join(os.getcwd())
FILE_PATH = os.path.join(UPLOAD_FOLDER, 'plix_credentials.json')

# Step 1: Create the Flask App
app = Flask(__name__)
CORS(app)

# Create a threading event that we'll use to notify the main thread
file_saved_event = threading.Event()

@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        
        # Save the JSON data to a file
        with open(FILE_PATH, 'w') as f:
         json.dump(data, f, indent=4) 
         # Save the JSON data to a file
         
        print(f'File saved at {FILE_PATH}')
        
        # Notify the main thread that the file has been saved
        file_saved_event.set()

        # Return response
        return jsonify({'status': 'success', 'message': 'Data saved successfully', 'file_path': FILE_PATH}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Step 2: Function to start Flask server in a separate thread
def run_flask_server():
    app.run(debug=False, port=5002, use_reloader=False)

def shutdown_server():
    """Shut down the Flask server."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# Step 3: Wrapper for starting the server in a thread
class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5002, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print("Starting server")
        self.srv.serve_forever()

    def shutdown(self):
        print("Shutting down server")
        self.srv.shutdown()


# Step 4: Main script logic
def main():
    # Check if the file already exists
    if not os.path.exists(FILE_PATH):
        print(f'{FILE_PATH} does not exist. Starting the Flask server to receive data...')

        # Start the Flask server in a separate thread
        server = ServerThread()
        server.start()

        # Open the browser at the desired URL
        #url = "http://127.0.0.1:5000"
        url="https://computo.dev/signin"

        print(f"Opening browser at {url}...")
        webbrowser.open_new_tab(url)  # Open a new tab with the specified URL

        # Wait until Flask signals that the file has been saved
        print("Waiting for Flask to notify file save...")
        file_saved_event.wait()  # This will block until `file_saved_event.set()` is called

        # Flask has notified that the file has been saved, now shut down the server
        server.shutdown()
        print("Flask server shut down.")

    # Continue with the rest of your script
    print("Continuing with the rest of the script...")


if __name__ == '__main__':
    main()

