En tant que programmeur, je veux une base de données pour pouvoir stocker sur l'ordinateur de l'utilisateur les aliments
d'openfoodfact dont il veut connaître un substitut plus sein

## tâche 1: 
- [X] Choisir quelles catégories pour la base de données:
  - categories
  - aliments
  - subsituts_enregistrés

## tâche 2:
- [X]  Définir les colonnes et tables de la base de données:

##### table catégories:

| id | nom_catégorie |
| --- | --- |
##
##### table aliments:

| id | nom_aliment | id_catégorie | magasin_le_vendant | lien_openfoodfact | note nutritionnelle |
| --- | --- | --- | --- | --- | --- |


##### table subsituts_enregistrés:

| id | nom_substitut | id_aliment_substitué | magasin_le_vendant | lien_openfoodfact | note nutritionnelle |
| --- | --- | --- | --- | --- | --- |

## tâches 3 et 4:
- [X] Ecrire la documentation pour chacune des requêtes SQL que je souhaite faire pour créer ma base de données et Ecrire le code SQL pour réaliser ces requêtes

Cette requête créée la table catégorie contenant les catégories de produits que l'utilisateur pourra chercher et ayant pour colonnes id et categories_names
```SQL
CREATE TABLE IF NOT EXISTS categories (
    id int(20) NOT NULL PRIMARY KEY,
    categories_names varchar(40) NOT NULL
) 
ENGINE=InnoDB;
```

Cette requête créée la table aliment contenant les aliments que l'utilisateur voudra substituer.
Elle aura pour colonnes id, aliments_names, categories_id, aliment_description, where_to_buy, OpenFoodFact_link
```SQL
CREATE TABLE IF NOT EXISTS aliments (
    id int(50) NOT NULL PRIMARY KEY,
    aliments_names varchar(50) NOT NULL,
    categories_id int(50) NOT NULL,
    aliment_description varchar(150) NULL,
    where_to_buy varchar(150) NOT NULL,
    OpenFoodFact_link varchar(80) NOT NULL,
    nutrition_grade char(1) NOT NULL
)
ENGINE=innoDB;
```

Cette requête créée la table aliment contenant les aliments que l'utilisateur voudra substituer.
Elle aura pour colonnes id, aliments_names, categories_id, aliment_description, where_to_buy, OpenFoodFact_link
```SQL
CREATE TABLE IF NOT EXISTS substitus_enregistrés (
    id int(50) NOT NULL PRIMARY KEY,
    nom_substitut varchar(50) NOT NULL,
    id_aliment_substitué int(50) NOT NULL,
    aliment_description varchar(150) NULL,
    where_to_buy varchar(150) NOT NULL,
    OpenFoodFact_link varchar(80) NOT NULL,
    nutrition_grade char(1) NOT NULL
)
ENGINE=innoDB;
```
