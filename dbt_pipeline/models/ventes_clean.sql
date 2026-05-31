select
    date,
    produit,
    categorie,
    quantite,
    prix_unitaire,
    ville,
    quantite * prix_unitaire as chiffre_affaires
from ventes_raw
where quantite > 0 and prix_unitaire > 0