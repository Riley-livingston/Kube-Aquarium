from flask import Flask, jsonify
from flask_cors import CORS
from kubernetes import client, config
import random  # For simulating data, remove in production
import logging

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Enable logging for detailed debug information
logging.basicConfig(level=logging.DEBUG)

# Explicitly load the in-cluster configuration to ensure the correct ServiceAccount is used
try:
    config.load_incluster_config()
    logging.info("Successfully loaded in-cluster config")
except Exception as e:
    logging.error(f"Error loading in-cluster config: {str(e)}")

# Initialize Kubernetes clients
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()

# Helper function to generate mock fish data
def generate_fish_data(num_fish=5):
    fish_data = []
    for i in range(num_fish):
        fish = {
            "id": f"fish-{i+1}",
            "species": random.choice(["Goldfish", "Betta", "Guppy"]),
            "health": random.randint(50, 100),
            "position": {"x": random.randint(0, 100), "y": random.randint(0, 100)}
        }
        fish_data.append(fish)
    return fish_data

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Aquarium Manager API"}), 200

@app.route('/api/dashboard_data')
def dashboard_data():
    try:
        # Get pod information with correct permissions
        pods = v1.list_namespaced_pod(namespace='default', label_selector='app=fish')
        total_pods = len(pods.items) if pods.items else 0  # Safeguard if no pods are found
        healthy_pods = sum(1 for pod in pods.items if pod.status.phase == 'Running')
        
        # Simulated CPU and memory usage (replace with real data if available)
        cpu_usage = random.uniform(0, 100) if total_pods > 0 else 0  # Safeguard: Avoid undefined
        memory_usage = random.uniform(0, 100) if total_pods > 0 else 0  # Safeguard: Avoid undefined
        
        # Return the data in the expected format
        return jsonify({
            "fishCount": total_pods,  # Total number of fish pods
            "cpuUsage": cpu_usage,  # Simulated CPU usage
            "memoryUsage": memory_usage,  # Simulated memory usage
            "healthyPods": healthy_pods,  # Healthy pods
            "totalPods": total_pods  # Total pods
        })
    except client.exceptions.ApiException as e:
        logging.error(f"APIException: {e}")
        return jsonify({"error": f"APIException: {e.reason}, Message: {e.body}"}), e.status
    except Exception as e:
        logging.error(f"General Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/aquarium_status')
def aquarium_status():
    try:
        # Use generate_fish_data to simulate fish status
        fish_data = generate_fish_data(num_fish=5)  # Simulate 5 fish
        return jsonify({
            "status": "healthy",
            "fish": fish_data,  # Return the fish data
            "waterQuality": "good"
        })
    except Exception as e:
        logging.error(f"General Exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)