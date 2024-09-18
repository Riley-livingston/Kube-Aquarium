import random
import time
import kubernetes
from kubernetes import client, config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load in-cluster Kubernetes configuration
try:
    config.load_incluster_config()
except config.ConfigException:
    logger.warning("Unable to load in-cluster config. Falling back to local config.")
    config.load_kube_config()

# Create Kubernetes API client
api = client.AppsV1Api()
core_api = client.CoreV1Api()

def simulate_population_change():
    try:
        deployment = api.read_namespaced_deployment(name="fish-deployment", namespace="default")
        current_replicas = deployment.spec.replicas
        new_replicas = max(1, current_replicas + random.choice([-1, 1]))
        deployment.spec.replicas = new_replicas
        api.patch_namespaced_deployment(name="fish-deployment", namespace="default", body=deployment)
        logger.info(f"Population changed. New number of fish: {new_replicas}")
    except kubernetes.client.exceptions.ApiException as e:
        logger.error(f"Error changing population: {e}")

def simulate_fish_sickness():
    try:
        deployment = api.read_namespaced_deployment(name="fish-deployment", namespace="default")
        container = deployment.spec.template.spec.containers[0]
        container.resources.limits['cpu'] = '100m'
        container.resources.limits['memory'] = '128Mi'
        api.patch_namespaced_deployment(name="fish-deployment", namespace="default", body=deployment)
        logger.info("Fish sickness simulated. Resources reduced.")
    except kubernetes.client.exceptions.ApiException as e:
        logger.error(f"Error simulating fish sickness: {e}")

def simulate_predator():
    try:
        pods = core_api.list_namespaced_pod(namespace="default", label_selector="app=fish")
        if pods.items:
            victim = random.choice(pods.items)
            core_api.delete_namespaced_pod(name=victim.metadata.name, namespace="default")
            logger.info(f"Predator attacked! Pod {victim.metadata.name} deleted.")
    except kubernetes.client.exceptions.ApiException as e:
        logger.error(f"Error simulating predator attack: {e}")

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