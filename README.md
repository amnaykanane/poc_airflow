# POC Airflow

4 tâches :
- T0 : Télécharger la donnée : 10 csvs contenant 100 nombres entiers
    - (en vrai c'est un sleep car les données sont en local)   
- T1* : Effectuer la somme des nombres
- T2* : Effectuer deux fois la somme des nombres
- T3 : Effectuer la division du résultat de T2 par celui de T1 (résultat attendu = 2)

*T1 et T2 sont effectuées en parallèle

## Lancer l'application
``docker-compose -f docker-compose.yaml up -d``

## WebServer
http://localhost:8080/ / username & password : airflow

## Flower 
http://localhost:5555/

## Résultat
Dans la vue graph, cliquer sur la dernière tâche puis log
