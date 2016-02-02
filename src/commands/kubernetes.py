import sys
import os
from gcloud import gcloud
from ManifestFactory import ManifestFactory
import json

class kubernetes:
    def __init__(self, subprocess):
        self.subprocess = subprocess
        self._cli = gcloud(subprocess).get_container() + ["kubectl"]

    def status(self, parameters):
        namespace = "--namespace=" + parameters["namespace"]
        print "\n\033[92mSERVICES\n\033[0m"
        self.subprocess.check_call(self._cli + ["get", "services", namespace])
        print "\n\033[92mRC\n\033[0m"
        self.subprocess.check_call(self._cli + ["get", "rc", namespace])
        print "\n\033[92mPODS\n\033[0m"
        self.subprocess.check_call(self._cli + ["get", "pods", namespace])
        print "\n\033[92mENDPOINTS\n\033[0m"
        self.subprocess.check_call(self._cli + ["get", "endpoints", namespace])
        print "\n\033[92mINGRESS\n\033[0m"
        self.subprocess.check_call(self._cli + ["get", "ingress", namespace])
        print "\n\033[92mNODES\n\033[0m"
        self.subprocess.check_call(self._cli + ["get", "nodes", namespace])

    def namespaces(self, parameters):
        self.subprocess.check_call(self._cli + ["get", "ns"])

    def cli(self, parameters):
        command = parameters["parameters"] if "parameters" in parameters else []
        try:
            self.subprocess.check_call(self._cli + command)
        except self.subprocess.CalledProcessError:
            sys.exit(1)

    def create_environment(self, parameters):
        manifest_factory = ManifestFactory()
        manifest = manifest_factory.new_namespace(parameters)
        output = json.dumps(manifest)

        path = '/hive_share/kubernetes'
        if not os.path.exists(path):
            os.makedirs(path)

        with open(path + '/namespace.yml', 'w') as f:
            f.write(output)

        self.subprocess.check_call(self._cli + ["create", "-f", path + "/namespace.yml"])

    def delete(self, args):
        self.subprocess.check_call(self._cli + ["delete", "ns", args["name"]])
