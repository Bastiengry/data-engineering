# Exécuter l'environnement

- Exécutez la commande : docker-compose up -d --build
- Patientez 2 à 3 minutes.
- Ouvrez votre navigateur web à l'adresse http://localhost:8080 (Airflow).
- Connectez-vous avec admin / admin.
- Lancez le DAG 01_simulate_sales pour (ré)générer le fichier de données.
- Lancez le DAG 02_process_sales_dag pour agréger les données et les ajouter à Clickhouse.
- Lancez le DAG 03_transform_sales_dbt pour traiter les données avec les modèles dbt.

# Vérifier le résultat

- Aller sur Clickhouse : http://localhost:8123/play
- Se connecter à la base de données :
  - Serveur : http://localhost:8123
  - Utilisateur : datamart      (==> à écrire à la place de default)
  - Mot de passe : datamart
  - Pour voir le résultat de la copie des données **agrégées** par Spark dans Clickhouse :
    ```sql
    SELECT * FROM datamart.sales_summary;
    ```
  - Pour voir le résultat de la copie des données **transformées** par dbt dans Clickhouse :
    ```sql
    SELECT * FROM datamart.stg_sales;         -- 1ere tranformation (staging)
    SELECT * FROM datamart.mart_top_stores;   -- 2nde tranformation (mart)
    ```
