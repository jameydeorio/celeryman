#!groovy
/* This file is automatically created by the `regen` command.
   To make changes please edit the `jenkins` key in your `application.json` file.
   See https://devdocs.platform-dev.gcp.oreilly.com/chassis/builds_and_deployment.html#configuring-your-jenkins-pipeline
*/

REGISTRY = 'gcr.io/common-build'
GCR_CREDENTIALS = 'gcr:gcr-common-build'
CHASSIS = 'gcr.io/common-build/chassis:latest'
GITHUB_REPO = 'git@github.com:oreillymedia/celeryman.git'
COMMIT_STATUS_SOURCE = 'jenkins/celeryman'
IMAGE_BASE_NAME = 'celeryman'
NAMESPACE = 'celeryman'
STABLE_BRANCH = 'master'
PUBLISHED_BRANCHES = ['master']
DEPLOY_STABLE_TO = ['dev-gke']
DEPLOY_RELEASES_TO = ['prod-gke']




def isRelease() {
  return env.IMAGE_TO_RELEASE ? true : false
}

node('kubectl2') {
  docker.withRegistry("https://${REGISTRY}", "${GCR_CREDENTIALS}") {
    stage('Initialize') {
      loadImage = CHASSIS
      if (isRelease()) {
        imageTag = env.IMAGE_TO_RELEASE.replace('image-', '')
        loadImage = "${REGISTRY}/${IMAGE_BASE_NAME}--manage:${imageTag}"
      }

      sh "docker pull ${loadImage}"
      sh "docker run --rm -e JENKINS=true ${loadImage} python /orm/manage.py cat Jenkinsfile.base > Jenkinsfile.base"
    }

    load 'Jenkinsfile.base'
  }
}
