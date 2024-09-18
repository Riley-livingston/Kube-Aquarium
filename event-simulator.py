import random
import time
import kubernetes
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create Kubernetes API client
api = client.AppsV1Api()

def simulate_population_change():
    # Randomly increase or decrease the number of fish
    change = random.choice([-1, 1])
    deployment = api.read_namespaced_deployment(name="fish-deployment", namespace="default")
    current_replicas = deployment.spec.replicas
    new_replicas = max(1, current_replicas + change)
    deployment.spec.replicas = new_replicas
    api.patch_namespaced_deployment(name="fish-deployment", namespace="default", body=deployment)
    print(f"Population changed. New number of fish: {new_replicas}")

def simulate_fish_sickness():
    # Simulate a fish getting sick by reducing its resources
    deployment = api.read_namespaced_deployment(name="fish-deployment", namespace="default")
    container = deployment.spec.template.spec.containers[0]
    container.resources.limits['cpu'] = '100m'
    container.resources.limits['memory'] = '128Mi'
    api.patch_namespaced_deployment(name="fish-deployment", namespace="default", body=deployment)
    print("Fish sickness simulated. Resources reduced.")

def simulate_predator():
    # Simulate a predator by deleting a random pod
    pods = client.CoreV1Api().list_namespaced_pod(namespace="default", label_selector="app=fish")
    if pods.items:
        victim = random.choice(pods.items)
        client.CoreV1Api().delete_namespaced_pod(name=victim.metadata.name, namespace="default")
        print(f"Predator attacked! Pod {victim.metadata.name} deleted.")

def main():
    while True:
        event = random.choice(['population', 'sickness', 'predator'])
        if event == 'population':
            simulate_population_change()
        elif event == 'sickness':
            simulate_fish_sickness()
        else:
            simulate_predator()
        time.sleep(60)  # Wait for 1 minute before next event

if __name__ == '__main__':
    main()
