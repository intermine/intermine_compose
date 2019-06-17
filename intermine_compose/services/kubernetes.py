from kubernetes import client, config

def init_kubernetes(app):
    config.load_kube_config(app.config["KUBERNETES_CONFIG_PATH"])


