# diagram.py
from diagrams import Diagram, Cluster, Edge

from diagrams.programming.language import Python
from diagrams.onprem.vcs import Git, Github
from diagrams.onprem.container import Docker

with Diagram("Cloud native CI", show=False):
    app = Git("app")
    with Cluster("Continuous integration pipeline"):
        repository = Github("repository")
        pylint = Python("pylint")
        pytest = Python("pytest")
        registry = Docker("registry")

    app >> Edge(label="push commit", style="dashed") >> repository 
    repository >> Edge(label="linter") >> pylint 
    pylint >> Edge(label="unit tests") >> pytest 
    pytest >> Edge(label="build image") >> registry