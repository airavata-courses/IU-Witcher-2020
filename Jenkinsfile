node{

    stage( "Checking into the respective branch of interest" ){
        git branch: 'docker-api-gateway', credentialsId: 'git-creds', url: 'https://github.com/airavata-courses/IU-Witcher-2020/'
    }

    stage( "Building of Docker Image" ){
         sh "docker build -t iuwitcher2020/dockerized_api_gateway:latest ."
    }

    stage('Pushing Built Docker Image to DockerHub'){
        withCredentials([string(credentialsId: 'secret-pwd', variable: 'dockerHubP')]){
     sh "docker login -u iu_witcher_2020 -p Password@123"
        }

  sh "docker push iuwitcher2020/dockerized_api_gateway:latest"
    }
    stage( 'Kuberenets Instance Cluster SSH into' ){
        cd "/dockerized_api_gateway"
        chmod 400 iu_witcher_2020.pem
        ssh -o StrictHostKeyChecking=no -i iu_witcher_2020.pem ubuntu@149.165.170.140  uptime
        ssh -i iu_witcher_2020.pem ubuntu@149.165.170.140  " rm -rf IU-Witcher-2020 &&
        git clone -b kubernetes_config https://github.com/airavata-courses/IU-Witcher-2020.git &&
        cd IU-Witcher-2020 &&
        cd dockerized_api_gateway && 
        export KUBECONFIG=/etc/kubernetes/admin.conf
        kubectl delete service &&
        kubectl delete deployment gateway-api &&
        kubectl apply -f config.yaml"
    }
}
