# diagram.py
from diagrams import Diagram, Cluster, Edge

from diagrams.programming.language import Python
from diagrams.onprem.vcs import Git, Github
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.cd import Tekton

with Diagram("Cloud native CD", show=False):

    with Cluster("Continuous deployment pipeline - production environment"):
        app = Git("app")
        infra_prod = Terraform("prod")
        pytest = Python("pytest")
        registry = Docker("registry")
        cd = Tekton("cd")

        app >> Edge(label="pull request", style="dashed") >> registry 
        registry >> Edge(label="update image", style="dashed") >> cd 
        cd >> Edge(label="provision prod infra") >> infra_prod
        infra_prod >> Edge(label="integration tests") >> pytest 
        pytest >> Edge(label="build image prod tag") >> registry

    with Cluster("Continuous deployment pipeline - staging environment"):
        app = Git("app")
        infra_stage = Terraform("stage")
        pytest = Python("pytest")
        registry = Docker("registry")
        cd = Tekton("cd")

        app >> Edge(label="pull request into stage", style="dashed") >> registry 
        registry >> Edge(label="update image", style="dashed") >> cd 
        cd >> Edge(label="provision stage infra") >> infra_stage
        infra_stage >> Edge(label="integration tests") >> pytest 
        pytest >> Edge(label="build image prod tag") >> registry

    with Cluster("Continuous deployment pipeline - development environment"):
        app = Git("app")
        infra_dev = Terraform("dev")
        pytest = Python("pytest")
        registry = Docker("registry")
        cd = Tekton("cd")

        app >> Edge(label="push commit into master", style="dashed") >> registry 
        registry >> Edge(label="update image", style="dashed") >> cd 
        cd >> Edge(label="provision dev infra") >> infra_dev
        infra_dev >> Edge(label="integration tests") >> pytest 
        pytest >> Edge(label="build image stage tag") >> registry
        
