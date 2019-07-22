from kubernetes import client, config
import os

def init_kubernetes(app):
    if os.environ.get("KUBE_ENABLE", default=True):
        if os.environ.get("FLASK_CONFIG_MODE", default=False) is "production": 
            config.load_incluster_config()
        else:
            pass
            config.load_kube_config(app.config["KUBERNETES_CONFIG_PATH"])


