FROM jenkins/jenkins:latest
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV CASC_JENKINS_CONFIG /var/jenkins_home/casc.yaml
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

USER root

#Install Python for semantic release
RUN apt-get update
RUN apt-get install python3 python3-pip ca-certificates curl gnupg -y
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED

# INSTALL docker to run locally
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN chmod a+r /etc/apt/keyrings/docker.gpg
RUN echo \
     "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
     "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
     tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt-get install docker-ce-cli -y

#Install Semantic Release
RUN pip install python-semantic-release

#Install zip
RUN apt-get install zip -y

#Install Github-Release gh (inbuilt of Github)
RUN apt-get install gh -y

#Install Gcloud to use command line gcloud commands
RUN echo "deb http://packages.cloud.google.com/apt cloud-sdk-stretch main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update -y && apt-get install google-cloud-sdk -y \
    && PATH=$PATH:/root/google-cloud-sdk/bin

#Install kubectl
RUN apt-get install -y apt-transport-https gnupg \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && echo 'deb https://apt.kubernetes.io/ kubernetes-xenial main' | tee -a /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update \
    && apt-get install -y kubectl

#Install gke-gcloud-auth-plugin for kubectl
RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update && apt-get install -y google-cloud-sdk-gke-gcloud-auth-plugin

#Install helm
RUN apt-get install -y wget \
    && wget https://get.helm.sh/helm-v3.7.0-linux-amd64.tar.gz \
    && tar -zxvf helm-v3.7.0-linux-amd64.tar.gz \
    && mv linux-amd64/helm /usr/local/bin/helm

#Install Go
RUN apt-get install -y golang

USER jenkins
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
#COPY github-key /var/jenkins_home/github-key
COPY casc.yaml /var/jenkins_home/casc.yaml
COPY webapp.groovy /usr/local/webapp.groovy
COPY webapp-db.groovy /usr/local/webapp-db.groovy
COPY webapp-helm-chart.groovy /usr/local/webapp-helm-chart.groovy
COPY helm-dependencies.groovy /usr/local/helm-dependencies.groovy
COPY health-check-results.groovy /usr/local/health-check-results.groovy
COPY perform-health-check.groovy /usr/local/perform-health-check.groovy
COPY health-check-operator.groovy /usr/local/health-check-operator.groovy