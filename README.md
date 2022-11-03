# BGMS Frontend Setup

C: qabristan/bgms>  
1- git init
2- git add .
3- git commit -m "First commit for bgms-frontend"
4- git remote add origin https://github.com/muhammadabdulhaseeb075/BGMS-Frontend.git
5- git branch -M main
6- git push -u origin main
7- Add credentials:  Username: saved in vm notepad
                     Password: saved in vm notepad


Repo

**Note:** Service Workers are only meant to work over secure origins, a.k.a. HTTPS. For development purposes they are also enabled to work on `localhost/` but it seems that `*.localhost` has been overlooked. This means that to get Service Workers to work you'll have to modify the `main_burialgroundsite` table in the `public` schema so that the `domain_url` of one of the client sites is simply `localhost`.
