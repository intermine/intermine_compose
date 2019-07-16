from kubernetes import client, config
import os

def init_kubernetes(app):
    if os.environ.get("FLASK_CONFIG_MODE", default=False) is not "production": 
        config.load_kube_config(app.config["KUBERNETES_CONFIG_PATH"])
    else:
        config.load_incluster_config()


