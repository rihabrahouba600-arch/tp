Question 1 : Pourquoi l'approche structurée (dlt + dbt + Dagster) est-elle supérieure à une 
approche artisanale (scripts Python isolés) ? 
L'approche structurée apporte des garanties indispensables pour un projet de production 
(DataOps) : 
• Idempotence : Contrairement à un script artisanal qui risque d'insérer des doublons à 
chaque exécution, l'approche structurée sépare strictement les couches de données 
(ventes_raw et ventes_clean), permettant de rejouer le pipeline à l'infini sans 
corrompre l'historique source. 
• Qualité et gouvernance : Les contrôles et validations sont automatisés à chaque 
étape, ce qui empêche une donnée corrompue d'atteindre les rapports décisionnels 
finaux. 
• Orchestration et traçabilité : Au lieu de lancer manuellement des scripts dans un 
ordre incertain, Dagster gère centralement les dépendances, offre un suivi visuel des 
pannes et conserve des logs détaillés de chaque exécution. 


Question 2 : Quel est l'intérêt d'utiliser DuckDB pour le stockage local et dlt pour 
l'ingestion ? 
• DuckDB : C'est une base de données analytique (orientée colonne) optimisée pour les 
requêtes complexes et les gros volumes de données. Son grand avantage est qu'elle 
s'exécute localement dans un fichier unique (comme un SQLite pour la Data), offrant 
des performances impressionnantes sans nécessiter l'infrastructure lourde d'un 
serveur Cloud (Snowflake, BigQuery). 
• dlt (data load tool) : Cet outil standardise et simplifie l'ingestion de données depuis 
des sources variées (APIs, fichiers, bases de données). Il gère automatiquement 
l'inférence et l'évolution des schémas (si une colonne s'ajoute ou change de type) et 
structure proprement les données dans DuckDB sans effort de code. 


Question 3 : Quel est le rôle de dbt dans ce projet ? Expliquez l'organisation en couches et 
l'importance de la macro {{ ref(...) }}. 
• Le rôle de dbt : dbt (data build tool) s'occupe exclusivement de la partie 
Transformation du pipeline (le "T" de l'ELT). Il permet aux Data Engineers d'écrire des 
transformations en langage SQL propre, tout en y associant des tests de qualité et 
une documentation automatisée. 
• L'organisation en couches (Architecture Medallion) : Les données progressent à 
travers des niveaux de maturité : 
o Bronze (Raw) : Données brutes identiques à la source. 
o Silver (Clean) : Données nettoyées, typées et filtrées (ventes_clean). 
o Gold (Mart/Resume) : Données agrégées prêtes pour les besoins métiers et la 
BI (ventes_resume). 
• L'importance de {{ ref(...) }} : Cette macro est le cœur de dbt. Elle permet de ne pas 
écrire le nom des tables "en dur". dbt l'utilise pour : 
1. Résoudre dynamiquement le nom de la table selon l'environnement 
(développement ou production). 
2. Construire automatiquement le graphe de lignage (Lineage Graph) afin de 
savoir exactement dans quel ordre exécuter les modèles SQL selon leurs 
dépendances. 


Question 4 : Comment Dagster orchestre-t-il l'ensemble ? Quelles sont les limites de 
l'utilisation de os.system() pour exécuter dbt ? 
• L'orchestration par Dagster : Dagster organise le pipeline sous forme de "Software
Defined Assets". Il sait exactement quel script Python produit quelle table. La 
topologie et l'ordre d'exécution (ingest $\rightarrow$ validate $\rightarrow$ 
transform $\rightarrow$ test_data) sont définis logiquement par les dépendances 
déclarées entre ces composants au sein du code de l'orchestrateur. 
• Les limites de os.system() : L'utilisation de os.system() pour appeler dbt est une 
solution transitoire peu recommandée en production car : 
o Elle masque les détails de l'exécution : l'orchestrateur voit uniquement si la 
commande globale a réussi ou échoué, mais il ne peut pas analyser finement 
quelle table spécifique de dbt a posé problème. 
o Elle empêche le partage natif des métadonnées, des logs détaillés et des 
artefacts entre les différentes boîtes du pipeline. 


Question 5 : Quel est le rôle de la CI (GitHub Actions) configurée à l'étape 6 ? Décrivez un 
scénario où elle échouerait. 
• Le rôle de la CI (Intégration Continue) : Le workflow GitHub Actions agit comme un 
garde-fou automatisé. À chaque fois qu'un développeur propose une modification 
(push ou pull request), un serveur distant rejoue les tests, installe les dépendances et 
compile le projet pour s'assurer que les modifications n'introduisent aucune 
régression ou erreur avant le déploiement. 
• Scénario d'échec : Imaginons qu'un développeur modifie le fichier pipeline/ingest.py 
et oublie par mégarde de fermer une parenthèse ou commette une erreur 
d'indentation. 
Lors du git push, GitHub Actions va déclencher le workflow. Arrivé à l'étape de vérification 
syntaxique (python -m py_compile), le compilateur lèvera une erreur. Le pipeline de CI 
passera instantanément au rouge, bloquant ainsi l'intégration d'un code cassé dans la 
branche principale (main).
