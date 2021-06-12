# HABITECH - Habit App

## What is this project about?
```
This repository is the backend of our habit app. The technology used is listed below:
1. Software stack: **Python-FastAPI**. This is a a REST framework that can make backend endpoints become easier to develop.
2. Database: **mongodb**. Mongodb is a non-sql database, we use JSON-like data entry to store all of our user data.
3. Machine Learning: **TODO: describe**
4. Cloud: **jenkins, k8s, many more**. We mirror this repository to Google Source Repository and use Jenkins to manage our CD. For now, only `canary` and `master` branch will be deployed to GKE upon running `git push`.
```

## Who are we?
```
Setiaki - A0101049@bangkit.academy
Hira - A0101023@bangkit.academy
Navi - M0101012@bangkit.academy
Alka - M0101050@bangkit.academy
Greg - C0101013@bangkit.academy
```


## Endpoints
Backend endpoint docs: https://api.habitbangkit.tech/docs <br/>
Alternative docs: https://api.habitbangkit.tech/redoc <br/>


## LOCAL Setup: how to run
To run this whole set of app on your local machine, you can do it manually or using container technology. This setup will guide you on running this app using the container technology on Ubuntu 20.04. 
1. Make sure docker and docker-compose is installed in your machine. You can try looking at the guide online.
2. Go to `mongodb-docker` directory and edit the `docker-compose.yaml` file using your favorite editor. You only need to change the `<CHANGE_HERE>` part with the path where you want the data of your database stored inside your computer.
3. Run this command inside the `mongodb-docker` folder. Remember this command is used in Ubuntu. For Windows user, find the equivalent command online.
```
sudo docker-compose up -d
```
4. At this point, you have a mongodb server ready to serve our backend app. Next, let's go to create docker image for our backend app. 
5. Go to root project directory (backend) where `Dockerfile` exist. Make sure you have the `.env` file. The file `example.env` is atemplate for out `.env` file. Next, we will build our `Dockerfile` into a docker image. We can do that by running the following command:
```
sudo docker build -t habit .
```
6. Check if the build is correct and the image is created successfully. After running this command, you should see that `habit` is listed. Here is the command:
```
sudo docker images
```
7. After making sure that `habit` image is listed, we will run our backend app. The following command will make a container from our `habit` image (a container is just an image that is being run):
```
sudo docker run -p 8080:8080 -d habit
```
8. Check if our backend is running by going to your favorite browser and go to `http://localhost:8080/docs`.

## LOCAL setup: how to clean up
This setup will guide you on stopping and cleaning this app if you set it up using the `how to run` steps above. 
1. Stop the running `habit` container. This will be run using 2 separate command. First, check the `CONTAINER ID` of our `habit` container, you can do this by running `sudo docker ps -a`. After that, copy the `CONTAINER ID` and run this command: `sudo docker container stop <CONTAINER_ID>`.
2. After stopping the container, we need to remove the container, run the following command:
```
sudo docker container rm <CONTAINER_ID>
```
3. If you want to also delete the image, run the following command:
```
sudo docker rmi habit
```
4. Turn off the mongodb service that we ran using docker-compose by using the following command:
```
sudo docker-compose stop mongodb
```
5. Additionally, if you want to, delete also the folder at the path you inserted inside the `Dockerfile`.
