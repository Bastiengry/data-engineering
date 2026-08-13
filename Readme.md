# Exécuter l'environnement

- Exécutez la commande : docker-compose up -d --build
- Patientez 2 à 3 minutes.
- Ouvrez votre navigateur web à l'adresse http://localhost:8080 (Airflow).
- Connectez-vous avec admin / admin.
- Lancez le DAG 01_simulate_sales pour (ré)générer le fichier de données.
- Lancez le DAG 02_process_sales_dag pour aggréger les données et les ajouter à la BDD PostgreSQL.

# Vérifier le résultat

- Aller sur le client SQL (adminer) : http://localhost:8081
- Se connecter à la base de données :
  - Système : PostgreSQL
  - Serveur : postgres-datamart
  - Utilisateur : datamart
  - Mot de passe : datamart
  - Base de données : datamart
  - Exécutez la requête "SELECT * FROM sales_summary;" pour voir les résultats.