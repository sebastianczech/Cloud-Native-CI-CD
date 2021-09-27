# diagram.py
from diagrams import Diagram, Cluster, Edge

from diagrams.programming.language import Python
from diagrams.onprem.vcs import Git, Github
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.cd import Tekton
from diagrams.k8s.ecosystem import Kustomize

with Diagram("Cloud native CD", show=False):
    app = Git("app")

    with Cluster("Continuous deployment pipeline - development environment"):
        infra_dev = Terraform("dev")
        pytest = Python("pytest")
        repository = Github("repository")
        registry = Docker("registry")
        k8s = Kustomize("k8s")
        cd = Tekton("cd")

        app >> Edge(label="push commit", style="dashed") >> repository 
        repository >> Edge(label="update image", style="dashed") >> cd 
        cd >> Edge(label="provision dev localstack") >> infra_dev
        infra_dev >> Edge(label="run app on dev") >> k8s 
        k8s >> Edge(label="integration tests") >> pytest 
        pytest >> Edge(label="build image stage tag") >> registry

    with Cluster("Continuous deployment pipeline - staging environment"):
        infra_stage = Terraform("stage")
        pytest = Python("pytest")
        repository = Github("repository")
        registry = Docker("registry")
        k8s = Kustomize("k8s")
        cd = Tekton("cd")

        app >> Edge(label="pull request into stage", style="dashed") >> repository 
        repository >> Edge(label="update image", style="dashed") >> cd 
        cd >> Edge(label="provision stage localstack") >> infra_stage
        infra_stage >> Edge(label="run app on stage") >> k8s 
        k8s >> Edge(label="integration tests") >> pytest 
        pytest >> Edge(label="build image prod tag") >> registry

    with Cluster("Continuous deployment pipeline - production environment"):
        infra_prod = Terraform("prod")
        pytest = Python("pytest")
        repository = Github("repository")
        registry = Docker("registry")
        k8s = Kustomize("k8s")
        cd = Tekton("cd")

        app >> Edge(label="pull request into master", style="dashed") >> repository 
        repository >> Edge(label="update image", style="dashed") >> cd 
        cd >> Edge(label="provision prod localstack") >> infra_prod
        infra_prod >> Edge(label="run app on prod") >> k8s 
        k8s >> Edge(label="integration tests") >> pytest 
        pytest >> Edge(label="build image lates tag") >> registry
