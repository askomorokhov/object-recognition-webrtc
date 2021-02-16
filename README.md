# object-recognition-webrtc


# Setup MongoDB using Docker

Run:
`docker run -d -p 27017:27017 --name some-mongo -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret mongo`

Connect:
`mongodb://mongoadmin:secret@localhost:27017/?ssl=false`


# Setup MongoDB using Minikube

 1. Install minikube https://minikube.sigs.k8s.io/docs/start/
 2. Start minikube `minikube start --nodes 3`
 2. Install PMM DBaaS
    - `docker pull percona/pmm-server:2 # Pull the latest 2.x image`
    - `docker create --volume /srv --name pmm-data percona/pmm-server:2 /bin/true` # Create a persistent data container.
    - `docker run --detach -e PERCONA_TEST_DBAAS=1 --restart always --publish 80:80 --publish 443:443 --volumes-from pmm-data --name pmm-server percona/pmm-server:2` # un the image to start PMM Server with enabled DBaaS.

3. Apply deployment:
    `kubectl apply -f deploy/psmdb-operator.yaml`
    `kubectl apply -f deploy/psmdb-secrets.yaml`

4. Get kube config `kubectl config view --minify --flatten`

5. Using UI register Minikube cluster and create MongoDB cluster.
