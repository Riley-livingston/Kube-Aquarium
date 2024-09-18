from flask import Flask, jsonify, request
from kubernetes import client, config
import requests

app = Flask(__name__)

# Load Kubernetes configuration
config.load_incluster_config()
api = client.AppsV1Api()
core_api = client.CoreV1Api()

def get_fish_pods():
    pods = core_api.list_namespaced_pod(namespace="default", label_selector="app=fish")
    return [pod.status.pod_ip for pod in pods.items if pod.status.pod_ip]

@app.route('/aquarium_status')
def get_aquarium_status():
    fish_pods = get_fish_pods()
    fish_statuses = []
    for pod_ip in fish_pods:
        try:
            response = requests.get(f"http://{pod_ip}:8080/status")
            fish_statuses.append(response.json())
        except requests.RequestException:
            pass
    return jsonify(fish_statuses)

@app.route('/scale', methods=['POST'])
def scale_fish():
    replicas = request.json.get('replicas')
    if not replicas:
        return jsonify({"error": "No replica count provided"}), 400
    
    try:
        deployment = api.read_namespaced_deployment(name="fish-deployment", namespace="default")
        deployment.spec.replicas = replicas
        api.patch_namespaced_deployment(name="fish-deployment", namespace="default", body=deployment)
        return jsonify({"message": f"Scaled to {replicas} replicas"})
    except client.ApiException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/simulate_event', methods=['POST'])
def simulate_event():
    event_type = request.json.get('event')
    if event_type == 'sickness':
        fish_pods = get_fish_pods()
        if fish_pods:
            target_pod = random.choice(fish_pods)
            try:
                requests.get(f"http://{target_pod}:8080/simulate_sickness")
                return jsonify({"message": "Simulated sickness event"})
            except requests.RequestException:
                return jsonify({"error": "Failed to simulate sickness"}), 500
    elif event_type == 'predator':
        try:
            pods = core_api.list_namespaced_pod(namespace="default", label_selector="app=fish")
            if pods.items:
                victim = random.choice(pods.items)
                core_api.delete_namespaced_pod(name=victim.metadata.name, namespace="default")
                return jsonify({"message": f"Simulated predator attack, deleted pod {victim.metadata.name}"})
            else:
                return jsonify({"message": "No fish to attack"})
        except client.ApiException as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Unknown event type"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)