from flask import Flask, request
import os
import json

from kubernetes import client, config

app = Flask(__name__)


# request counter
request_counter = {}

HELLO_WORLD = "/"
request_counter[HELLO_WORLD] = 0

# Requirement 1.2.


@app.route("/")
def hello():
    request_counter[HELLO_WORLD] += 1
    return "Hello World!"


@app.route("/greetings")
def greetings():
    # Requirement 1.3
    greeting = os.getenv("GREETING", "GREETING env var not set.")
    return greeting


@app.route("/listcontents")
def listcontents():
    # Requirement 1.3
    contents = os.listdir("/hostfolder")
    fp = open("/hostfolder/filenames.txt","r")
    lines = fp.readlines()
    return lines


@app.route("/getk8sobjects")
def get_cluster_details():
    # Requirement 1.3
    config.load_incluster_config()

    namespace = os.getenv("NAMESPACE")
    
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace)

    output = {}

    pod_names = []
    for pod in pods.items:
        pod_names.append(pod.metadata.name)
    output["pods"] = pod_names

    cfg_map_names = []
    configmaps = v1.list_namespaced_config_map(namespace)
    for configmap in configmaps.items:
        cfg_map_names.append(configmap.metadata.name)
    output["configmaps"] = cfg_map_names

    sa_names = []
    serviceaccounts = v1.list_namespaced_service_account(namespace)
    for serviceaccount in serviceaccounts.items:
        sa_names.append(serviceaccount.metadata.name)
    output["serviceaccounts"] = sa_names

    rbac_api = client.RbacAuthorizationV1Api()
    # Roles
    role_names = []
    roles = rbac_api.list_namespaced_role(namespace)
    for role in roles.items:
        role_names.append(role.metadata.name)
    output["roles"] = role_names
    
    # Rolebindings
    role_binding_names = []
    rolebindings = rbac_api.list_namespaced_role_binding(namespace)
    for rb in rolebindings.items:
        role_binding_names.append(rb.metadata.name)
    output["rolebindings"] = role_binding_names

    obj_to_return = json.dumps(output)
    return obj_to_return


# Requirement 1.4
# Implement "/metrics" endpoint


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
