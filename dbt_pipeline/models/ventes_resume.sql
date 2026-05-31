select
    categorie,
    sum(quantite) as total_quantite,
    sum(chiffre_affaires) as total_ca
from {{ ref('ventes_clean') }}
group by categorie