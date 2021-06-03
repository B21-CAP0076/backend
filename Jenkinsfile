pipeline {

  environment {
    PROJECT = "b21-cap0076"
    APP_NAME = "habit"
    BE_SVC_NAME = "${APP_NAME}-backend"
    CLUSTER = "backend-cluster"
    CLUSTER_ZONE = "asia-southeast1-b"
    IMAGE_TAG = "gcr.io/${PROJECT}/${APP_NAME}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
    JENKINS_CRED = "${PROJECT}"
  }

  agent none

  stages {
    stage('Build and push image with Container Builder') {
      agent {
            docker {
              image 'gcr.io/google.com/cloudsdktool/cloud-sdk'
              args "-u root"
            }
      }
      steps {
        withCredentials([file(credentialsId: 'key-sa', variable: 'GC_KEY1')]) {
          sh("echo GC_KEY:${GC_KEY1}")
          sh("gcloud auth activate-service-account 346784273889-compute@developer.gserviceaccount.com --key-file ${GC_KEY1} --project=${PROJECT}")
          sh("gsutil cp gs://habit-env-bucket/prod-env env_file")
          sh("chown cloudsdk:cloudsdk .env")
          sh("echo '' > .gitignore")
          sh "PYTHONUNBUFFERED=1 gcloud builds submit -t ${IMAGE_TAG} ."
        }
        
      }
    }
    stage('Deploy Canary') {
      // Canary branch
      when { branch 'canary' }
      agent {
        docker {
              image 'gcr.io/google.com/cloudsdktool/cloud-sdk'
              args "-u root"
            }
      }
      steps {
        withCredentials([file(credentialsId: 'key-sa', variable: 'GC_KEY2')]) {
          sh("gcloud auth activate-service-account 346784273889-compute@developer.gserviceaccount.com --key-file ${GC_KEY2} --project=${PROJECT}")
            // Change deployed image in canary to the one we just built
          sh("sed -i.bak 's#gcr.io/b21-cap0076/habit:1.0.0#${IMAGE_TAG}#' ./k8s/canary/*.yaml")
          sh("gcloud container clusters get-credentials backend-cluster --zone asia-southeast1-b --project b21-cap0076")
          sh("kubectl set image deployment habit-backend-canary *=${IMAGE_TAG} -n production")
          sh("kubectl rollout status deployment habit-backend-canary -n production")
        }
      }
    }
    stage('Deploy Production') {
      // Production branch`
      when { branch 'master' }
      agent {
        docker {
              image 'gcr.io/google.com/cloudsdktool/cloud-sdk'
              args "-u root"
            }
      }
      steps{
        withCredentials([file(credentialsId: 'key-sa', variable: 'GC_KEY3')]) {
          sh("gcloud auth activate-service-account 346784273889-compute@developer.gserviceaccount.com --key-file ${GC_KEY2} --project=${PROJECT}")
            // Change deployed image in canary to the one we just built
          sh("sed -i.bak 's#gcr.io/b21-cap0076/habit:1.0.0#${IMAGE_TAG}#' ./k8s/canary/*.yaml")
          sh("gcloud container clusters get-credentials backend-cluster --zone asia-southeast1-b --project b21-cap0076")
          sh("kubectl set image deployment habit-backend-production *=${IMAGE_TAG} -n production")
          sh("kubectl rollout status deployment habit-backend-production -n production")
        }
      }
    }
  }
}
