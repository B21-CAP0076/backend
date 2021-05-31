pipeline {

  environment {
    PROJECT = "b21-cap0076 "
    APP_NAME = "habit"
    BE_SVC_NAME = "${APP_NAME}-backend"
    CLUSTER = "jenkins-cd"
    CLUSTER_ZONE = "asia-southeast2-a"
    IMAGE_TAG = "gcr.io/${PROJECT}/${APP_NAME}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
    JENKINS_CRED = "${PROJECT}"
  }

  agent none
  stages {
    stage('Build and push image with Container Builder') {
      agent {
            docker { image 'gcr.io/cloud-builders/gcloud' }
      }
      steps {
        withCredentials([file(credentialsId: 'key-sa', variable: 'GC_KEY')]) {
          sh("gcloud auth activate-service-account --key-file=${GC_KEY}")
          sh("gsutil cp gs://habit-env-bucket/prod-env .env")
          sh "PYTHONUNBUFFERED=1 gcloud builds submit -t ${IMAGE_TAG} ."
        }
        
      }
    }
    stage('Deploy Canary') {
      // Canary branch
      when { branch 'canary' }
      agent {
        docker { image 'gcr.io/cloud-builders/kubectl' }
      }
      steps {
        withCredentials([file(credentialsId: 'key-sa', variable: 'GC_KEY')]) {
          sh("gcloud auth activate-service-account --key-file=${GC_KEY}")
            // Change deployed image in canary to the one we just built
          sh("sed -i.bak 's#gcr.io/b21-cap0076/habit:1.0.0#${IMAGE_TAG}#' ./k8s/canary/*.yaml")
          step([$class: 'KubernetesEngineBuilder', namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'k8s/services', credentialsId: env.JENKINS_CRED, verifyDeployments: false])
          step([$class: 'KubernetesEngineBuilder', namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'k8s/canary', credentialsId: env.JENKINS_CRED, verifyDeployments: true])
          sh("echo http://`kubectl --namespace=production get service/${BE_SVC_NAME} -o jsonpath='{.status.loadBalancer.ingress[0].ip}'` > ${BE_SVC_NAME}")
        }
      }
    }
    stage('Deploy Production') {
      // Production branch
      when { branch 'master' }
      agent {
        docker { image 'gcr.io/cloud-builders/kubectl' }
      }
      steps{
        withCredentials([file(credentialsId: 'key-sa', variable: 'GC_KEY')]) {
          sh("gcloud auth activate-service-account --key-file=${GC_KEY}")
          // Change deployed image in canary to the one we just built
          sh("sed -i.bak 's#gcr.io/b21-cap0076/habit:1.0.0#${IMAGE_TAG}#' ./k8s/production/*.yaml")
          step([$class: 'KubernetesEngineBuilder', namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'k8s/services', credentialsId: env.JENKINS_CRED, verifyDeployments: false])
          step([$class: 'KubernetesEngineBuilder', namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'k8s/production', credentialsId: env.JENKINS_CRED, verifyDeployments: true])
          sh("echo http://`kubectl --namespace=production get service/${BE_SVC_NAME} -o jsonpath='{.status.loadBalancer.ingress[0].ip}'` > ${BE_SVC_NAME}")
        }
      }
    }
  }
}
