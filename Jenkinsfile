node{

    stage( "Checking into the respective branch of interest" ){
        git branch: 'dockerized_model_execution', credentialsId: 'git-creds', url: 'https://github.com/airavata-courses/IU-Witcher-2020/'
    }

    stage( "Building of Docker Image" ){
         sh "docker build -t iuwitcher2020/dockerized_model_execution ."
    }

    stage('Pushing Built Docker Image to DockerHub'){
        withCredentials([string(credentialsId: 'secret-pwd', variable: 'dockerHubP')]){
     sh "docker login -u iu_witcher_2020 -p Password@123"
        }

  sh "docker push iuwitcher2020/dockerized_model_execution"
    }
}
