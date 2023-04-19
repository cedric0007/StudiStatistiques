# StudiStatistiques

Se placer dans le dossier et executer les commandes suivantes :
    studi_statistiques
	    docker build -t studi_statistiques .
        

Installation indépendant de l'application python puis connexion au mysql créé via le docker-compose
    docker network connect studistatistiques_default python_studi_statistiques

Installer les librairies manquantes :
    cd Modules/apiStatistiques/ && pip install python-jose[cryptography] passlib[bcrypt] && python app.py

Run :
    docker run --rm -it -d -p 0.0.0.0:8001:8001 --name python_studi_statistiques studi_statistiques:latest
    docker run --rm -it -d -p 81:8000 --name python_studi_statistiques studi_statistiques:latest

    docker run -d --name mycontainer -p 80:80 myimage


# Commandes utiles