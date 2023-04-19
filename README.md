# StudiStatistiques

Se placer dans le dossier et executer les commandes suivantes :
    studi_statistiques
	    docker build -t studi_statistiques .
        

Installation indépendant de l'application python puis connexion au mysql créé via le docker-compose
    docker network connect studistatistiques_default strange_goldwasser

Installer les librairies manquantes :
    pip install python-jose[cryptography] passlib[bcrypt]

Run :
    docker run --rm -it -d -p 8001:8000 --name python_studi_statistiques studi_statistiques:latest

# Commandes utiles