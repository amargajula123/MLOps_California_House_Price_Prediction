# MLOps_California_House_Price_Prediction
MLOps_California_House_Price_Prediction is an end-to-end machine learning project designed to predict house prices in California using modern MLOps practices. This project combines data science, model development, and deployment pipelines to create a scalable and reproducible housing price prediction system.


### Software and account Requirements


Application url:
[HousingPredictor](https://ml-regression-app.herokuapp.com/)
.

1. [Github Account](https://github.com)
2. [Heroku Account](https://dashboard.heroku.com/login)
3. [VS Code IDE](https://code.visualstudio.com/download)
4. [GIT cli](https://git-scm.com/downloads)
5. [GIT Documentation](https://git-scm.com/docs/gittutorial)


Creating conda environment 
```
1.conda create -p <environment_name> 
2.conda create -p venv python==3.9 -y
```

Discription about "-p" , "-n" and "Vertual Environment"
```
-p =  -p is the prefix if you use "-p" then your Vertual Environment(venv)
      will created inside your Current Working Dir

      if you use "-n" then your Vertual Environment(venv)
      will created where ever your "Anaconda" is installed,
      there it will going to install the Vertual Environment(venv)

venv = "folder", one folder gets created and inside that all the project
       required libraries getting stored which we installed,
```

for windows use this 
```
conda activate venv/
```
OR 
```
conda activate venv 
```

```
pip install -r requirements.txt
```

To clear the terminal screen 
```
cls
```

To Add files to git
```
git add .
```

OR
```
git add <file_name>
```

> Note: To ignore file or folder from git we can write name of file/folder in .gitignore file

To check the git status 
```
git status
```
To check all version maintained by git
```
git log
```

To create version/commit all changes in git
```
git commit -m "message"
```
To commit version/changes without doing any modification
```
git commit --allow-empty -m "Comment your wish"
``` 

To send version/changes to github
```
git push origin main
```

To check remote url 
```
git remote -v
```

To know the branch name 
```
git branch
```

To delete/remove the file from the git
```
git restore/remove <filename>
```

To setup CI/CD pipeline in heroku we need 3 information

1. HEROKU_EMAIL = amargknr@gmail.com
2. HEROKU_API_KEY = HRKU-50374ebf-b026-421f-a45a-ed64465edf89
3. HEROKU_APP_NAME = ml-app-test

To stop app

```
heroku ps:scale web=0 --app <app name>
```

BUILD DOCKER IMAGE
```
docker build -t <image_name>:<tagname> .

Ex :-
  docker build -t ml-project:new1 .
```
> Note: Image name for docker must be lowercase


To list docker image
```
docker images
```

Run docker image
```
docker run -p 5000:5000 -e PORT=5000 <f8c749e73678/id of image>
```

To check running container in docker
```
docker ps
```

Tos stop docker conatiner
```
docker stop <container_id>
```

gunicorn :=  #gunicorn which is used to run  flask 
          # application its basically designed for Linex based system 

```
python setup.py install
```


Install ipykernel for jupyter notebook

```
pip install ipykernel
```
what is stratified split ?
Ans :-
    what is the "data distribution" with respect to "training dataset" is to be equal to the
    "data distribution" with respect to "testing dataset" is called "stratified split"

why we are doing straitified split ?
ans :-
     when you train your model with the help of training dataset and we know training is the 
     representation of Population dataset, so after training our model
     we also need to perform test the model/evaluate with "test dataset", so it require that 
     the distribution of "test dataset" is also similer to the trainig dataset 

Data Drift:
When your "Datset" statistics gets change we call it as data drift

what we do in Data_draft ?

Ans:-
we try to check the statistics of one dataset with the another dataset if the
statistics of both dataset "are SAME" there is 0 "Data_drift".
if the statistics of both dataset "are NOT SAME" there will be "Data_drift".
bassically we  compare statistics of both datasets





## Write a function to get training file path from artifact dir
#hi

```
heroku stack:set container --app  {here you HEROKU APP NAME}
```
