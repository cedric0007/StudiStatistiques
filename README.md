# StudiStatistiques

Se placer dans le dossier et executer les commandes suivantes :
    studi_statistiques
	    docker build -t studi_statistiques .
        

Installation indépendant de l'application python puis connexion au mysql créé via le docker-compose
    docker network connect studistatistiques_default strange_goldwasser

Installer les librairies manquantes :
    pip install python-jose[cryptography] passlib[bcrypt]

