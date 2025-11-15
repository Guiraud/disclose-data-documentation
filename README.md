### [Disclose Data - Explorateur de données des autorités environnementales](https://data.disclose.ngo/explorateur-autorite-environnementale)

# Documentation API

## Table des matières

- [Démarrage rapide](#démarrage-rapide)
- [Généralités](#généralités)
- [Champs DocumentCloud](#champs-documentcloud)
- [Métadonnées des documents](#métadonnées-des-documents)
- [Exemples de requêtes](#exemples-de-requêtes)
- [Exports CSV](#exports-csv)
- [Ressources](#ressources)
- [FAQ](#faq)
- [Contact](#contact)

## Démarrage rapide

**Nouveau dans l'utilisation de cette API ?** Consultez notre [tutoriel pour débutants](tutorials/getting-started.md) qui vous guide pas à pas.

**Installation rapide :**
```bash
pip install python-documentcloud
```

**Exemple de code minimal :**
```python
from documentcloud import DocumentCloud

client = DocumentCloud()
results = client.documents.search('+project:219834 +status:"success"')

print(f"Nombre de documents : {results.count}")
for doc in results[:5]:
    print(f"- {doc.title}")
```

## Généralités

Les documents de Disclose Data sont en accès libre sur [DocumentCloud](https://documentcloud.fr), la plateforme de publication de documents de l'ONG [MuckRock](https://www.muckrock.com/).

Tous les documents sont rassemblés dans le projet intitulé "[Disclose Data - Explorateur AE](https://www.documentcloud.org/projects/219834/)" (id `219834`)

Vous pouvez donc y accéder soit par l'interface graphique de DocumentCloud, soit par son API, comme détaillé dans les pages de documentation suivantes :

- [DocumentCloud FAQ](https://www.documentcloud.org/help/faq/)
- [DocumentCloud Search](https://www.documentcloud.org/help/search/)
- [DocumentCloud API](https://www.documentcloud.org/help/api/)

Si vous utilisez le langage de programmation Python, nous recommandons d'utiliser la bibliothèque `python-documentcloud` ([documentation](https://documentcloud.readthedocs.io/en/latest/gettingstarted.html)).

## Champs DocumentCloud

Nous ne détaillons ici que les champs dont nous faisons une utilisation particulière. Pour les autres champs, référez-vous à la [documentation de DocumentCloud](https://www.documentcloud.org/help/api/#documents).

### `data`

*format : JSON*

Métadonnées personnalisées de notre collection de documents. Voir ["Métadonnées des documents"](#métadonnées-des-documents).


### `description`

*format : texte*

Nom du dossier auquel est rattaché le document. 
NB: Nous utilisons ce champ plutôt qu'une métadonnée personnalisée car ces dernières sont limitées à 300 caractères.

### `project`

*format : nombre entier*

Projet dans lequel se trouve les documents sur DocumentCloud. Tous nos documents se trouvent dans le même projet DocumentCloud (id `219834`), donc toutes vos requêtes doivent comporter `+project:219834`

### `publish_at`

*format: "YYYY-MM-DDThh:mm:ss.fZ"*

Date de publication du document sur le site cible. Ce champ permet l'utilisation des opérateurs de date de DocumentCloud (cf. [Specifiying Dates and Times](https://www.documentcloud.org/help/search/#specifying-dates-and-times)) qui permettent de restreindre la recherche à une certaine période.

NB : Pour classer les documents par date de publication, utilisez plutôt la métadonnée "publication_date".

### `status`

*format : texte*

Indique le statut de l’importation du document dans DocumentCloud. Le [site Disclose Data](https://data.disclose.ngo/explorateur-autorite-environnementale) n'affiche que les documents dont le status est `success`, nous vous conseillons de restreindre vos requêtes API de la même façon (`+status:"success"`)

## Métadonnées des documents

Ces métadonnées sont collectées par nos scrapers ou renseignées a posteriori. Elles peuvent être utilisées comme filtres de recherche en préfixant le nom de la métadonnée par `data_`, comme indiqué dans la [documentation de recherche DocumentCloud](https://www.documentcloud.org/help/search/#filter-fields).

Toutes les métadonnées sont au format texte. Pour une métadonnée, plusieurs valeurs sont possibles. Par exemple `departments` contient une liste de codes de départements concernés par le document.

### `authority`

Autorité environnementale chargée du dossier.

### `category`

Catégorie de procédure à laquelle appartient le document ("Cadrage", "Avis" ou "Cas par Cas"). Cf. [F.A.Q.](https://data.disclose.ngo/explorateur-autorite-environnementale/faq).

### `category_local`

Catégorie du document telle qu’elle apparaît sur le site source.

### `departments`

Liste de codes de départements ou de collectivités d’outre mer impactés par le dossier auquel se rattache le document.

### `departments_sources`

Méthode(s) utilisées pour classifier par départments. Valeurs possibles :
- `scraper`: quand le(s) code(s) de département est récupéré par le scraper
- `regex`: quand ils sont matchés par expression régulière d’après le titre du projet
- `authority`: quand ils sont déduits de l’autorité (exemple : "Préfecture de région Guyane")
- `gpt-4o` ou le nom du modèle d'IA si une IA a été utilisée
- `human`: quand ces codes ont été renseignés manuellement par l'équipe de Disclose Data.

### `event_data_key`

Clé unique du document. Permet aux scrapers d'ignorer les documents déjà importés dans DocumentCloud. Dans la plupart des cas, la valeur de ce champ équivaut à l'URL du document (`source_file_url`). Lorsque le document est issu d'un fichier .zip, le champ est constitué de l'URL du fichier .zip et du chemin du document dans ce zip (exemple : "https://site.com/fichier.zip/dossier1/dossier2/fichier.pdf")

### `project_id`

Identifiant du dossier auquel le document est rattaché. Cet identifiant est généré en concaténant la page source du dossier (métadonnée `source_page_url`) et son nom (champ `description`), puis en passant le tout dans une fonction de hachage SHA-256.

### `project_types_sources`

Méthode(s) utilisées pour clmassifier le document par type de projet. Valeurs possibles : 
- `gpt-4o` ou le nom du modèle d'IA si une IA a été utilisée.
- `human` quand le type de projet a été renseigné manuellement par l'équipe de Disclose Data.

### `publication_datetime`

Date et heure (UTC) de publication du document sur son site source.

### `publication_date`

Date de publication du document sur son site source.

### `publication_time`

Heure (UTC) de publication du document sur son site source.

### `source_scraper`

Nom du scraper qui a ajouté le document.

### `source_scraper_year`

Année visée par le scraper quand le document a été ajouté.

### `source_filename`

Nom original du fichier.

### `source_page_url`

URL de la page sur laquelle le document est mentionné.

### `source_file_url`

URL du document sur son site source.

### `_tag`

Tags additionnels du document. Certains documents sont temporairement cachés dans l'interface graphique par le tag `hidden`.


## Exemples de requêtes

### Tous les documents

`+project:219834`

⚠️ Les résultats contiendront des documents qui n'ont pas été importés correctement.

### Tous les documents affichés dans l'explorateur

`+project:219834 +status:"success" +created_at:[* TO NOW-2HOURS] -tag:"hidden"`

- `+created_at:[* TO NOW-2HOURS]` restreint la recherche aux documents importés il y a moins de 2 heures. Ce délai permet à nos add-ons de classification (par type, par département) de traiter les documents avant leur apparition sur le site.

### Tous documents liés à des projets de type "Travaux miniers"

`+project:219834 +data_project_types:"Travaux miniers"`

### Tous les documents publiés par l'autorité environnementale "Préfecture de région Bretagne"

`+project:219834 +status:"success" +data_authority:"Préfecture de région Bretagne"`

### Tous les documents contenant le mot "lithium"

`+project:219834 +status:"success" lithium`

### Tous les documents rattachés à des dossiers dont le nom contient "lithium"

`+project:219834 +status:"success" description:lithium`

### Tous les documents publiés entre le 1er janvier 2024 et le 31 janvier 2024 (inclus)

`+project:219834 +status:"success" +publish_at:["2024-01-01T00:00:00Z" TO "2024-02-01T00:00:00Z"]`

## Exports CSV

Si votre but est d'exporter des résultats de recherche au format .CSV, deux Add-Ons DocumentCloud facilitent cette tâche :
- [Metadata Grabber](https://www.documentcloud.org/add-ons/cam-garrison/documentcloud-metadata-grabber/)
- [Custom Metadata Scraper](https://www.documentcloud.org/add-ons/MuckRock/documentcloud-custom-metadata-scraper-addon/)

Vous trouverez une présentation en anglais de ces deux Add-Ons dans [cette vidéo YouTube](https://www.youtube.com/watch?v=YvJ4MU9Xheg) réalisée par MuckRock.

**Alternative :** Nous avons également créé des [scripts Python prêts à l'emploi](scripts/) pour exporter facilement vos données.

## Ressources

Ce dépôt contient de nombreuses ressources pour vous aider à utiliser l'API Disclose Data :

### 📚 [Tutoriel débutant](tutorials/getting-started.md)

Un guide complet pas-à-pas pour apprendre à utiliser l'API, parfait pour les débutants. Couvre :
- Installation et configuration
- Premières requêtes
- Filtrage des résultats
- Recherche avancée
- Export de données

### 💡 [Exemples de code](examples/)

6 exemples Python commentés pour apprendre par la pratique :
- `01_basic_search.py` - Recherche basique
- `02_filter_by_authority.py` - Filtrer par autorité
- `03_filter_by_department.py` - Filtrer par département
- `04_filter_by_date.py` - Filtrer par période
- `05_search_text.py` - Recherche textuelle
- `06_export_to_csv.py` - Export CSV

### 🛠️ [Scripts utilitaires](scripts/)

4 scripts en ligne de commande prêts à l'emploi :
- `search_documents.py` - Rechercher des documents interactivement
- `export_data.py` - Exporter vers CSV avec filtres
- `get_statistics.py` - Obtenir des statistiques détaillées
- `monitor_new_documents.py` - Surveiller les nouveaux documents

**Exemple d'utilisation :**
```bash
python scripts/search_documents.py --keyword éolien --department 35
python scripts/export_data.py --authority "Préfecture de région Bretagne" -o bretagne.csv
python scripts/get_statistics.py --year 2024
```

### 📊 [Visualisations](visualizations/)

5 scripts pour créer des graphiques et analyses visuelles :
- `01_timeline_visualization.py` - Évolution temporelle
- `02_geographic_distribution.py` - Distribution géographique
- `03_authority_analysis.py` - Analyse par autorité
- `04_category_breakdown.py` - Répartition par catégorie
- `05_comprehensive_dashboard.py` - Tableau de bord complet

### 📦 Installation des dépendances

Pour utiliser tous les exemples et scripts :

```bash
pip install -r requirements.txt
```

## FAQ

### Questions générales

**Q : Combien de documents sont disponibles dans la collection ?**

R : La collection contient plusieurs milliers de documents et est mise à jour régulièrement. Utilisez le script `get_statistics.py` pour obtenir le nombre exact actuel.

**Q : Les données sont-elles gratuites et librement accessibles ?**

R : Oui, tous les documents sont en accès libre via l'API DocumentCloud. Aucune authentification n'est requise pour consulter les documents.

**Q : À quelle fréquence la collection est-elle mise à jour ?**

R : La collection est mise à jour automatiquement par nos scrapers qui collectent les nouveaux documents publiés par les autorités environnementales. Utilisez le script `monitor_new_documents.py` pour suivre les ajouts récents.

### Questions techniques

**Q : Dois-je créer un compte DocumentCloud pour utiliser l'API ?**

R : Non, l'accès en lecture aux documents publics ne nécessite pas de compte. Un compte n'est nécessaire que si vous souhaitez uploader vos propres documents.

**Q : Y a-t-il des limites de taux (rate limits) sur l'API ?**

R : DocumentCloud applique des limites raisonnables pour éviter les abus. Pour de grandes quantités de requêtes, espacez vos appels et utilisez les filtres pour limiter le nombre de résultats.

**Q : Comment puis-je rechercher dans le contenu texte des documents ?**

R : DocumentCloud effectue une OCR automatique sur tous les documents PDF. Utilisez simplement votre mot-clé dans la requête (ex: `+project:219834 +status:"success" éolien`) pour chercher dans le contenu.

**Q : Comment télécharger les fichiers PDF originaux ?**

R : Chaque document a une URL accessible via `doc.canonical_url` (pour la page web) et les métadonnées contiennent `source_file_url` pour l'URL du PDF original sur le site source.

**Q : Puis-je filtrer par plusieurs départements à la fois ?**

R : Oui, utilisez l'opérateur OR :
```python
query = '+project:219834 +status:"success" (+data_departments:"35" OR +data_departments:"56")'
```

**Q : Comment obtenir tous les documents sans limitation ?**

R : Par défaut, les résultats sont paginés. Pour obtenir tous les documents, itérez sur tous les résultats :
```python
results = client.documents.search(query)
for doc in results:  # Itère automatiquement sur toutes les pages
    # Traiter le document
```

### Questions sur les métadonnées

**Q : Qu'est-ce que la différence entre `category` et `category_local` ?**

R : `category` est une classification standardisée par Disclose (Avis, Cadrage, Cas par Cas) tandis que `category_local` est le nom exact tel qu'il apparaît sur le site source.

**Q : Pourquoi certains documents n'ont pas de département assigné ?**

R : Certains projets peuvent concerner plusieurs régions ou l'ensemble du territoire. Les départements sont extraits automatiquement quand c'est possible, mais peuvent être absents dans certains cas.

**Q : Comment sont classifiés les départements ?**

R : Consultez la métadonnée `departments_sources` qui indique la méthode utilisée : scraper, regex, IA (GPT-4o), ou classification manuelle.

### Problèmes courants

**Q : J'obtiens 0 résultats alors que je devrais en avoir**

R : Vérifiez que :
- Vous incluez bien `+project:219834` dans votre requête
- Vous utilisez `+status:"success"` pour exclure les documents mal importés
- Vos filtres utilisent la syntaxe correcte (guillemets pour les valeurs avec espaces)
- Les noms d'autorités et catégories sont exacts (sensibles à la casse)

**Q : Comment déboguer mes requêtes ?**

R : Commencez par une requête simple et ajoutez les filtres progressivement :
```python
# Commencer simple
query = '+project:219834 +status:"success"'

# Ajouter un filtre à la fois
query += ' +data_authority:"Préfecture de région Bretagne"'
# etc.
```

**Q : Mes scripts Python sont lents**

R : Pour améliorer les performances :
- Limitez le nombre de résultats avec `results[:1000]`
- Utilisez des filtres spécifiques pour réduire le nombre de documents
- Évitez de charger tous les documents si vous n'avez besoin que de statistiques

### Support et contribution

**Q : J'ai trouvé une erreur dans les données, que faire ?**

R : Contactez-nous à data@disclose.ngo en précisant l'ID du document concerné et la nature du problème.

**Q : Puis-je contribuer à améliorer cette documentation ?**

R : Oui ! Nous acceptons les contributions. N'hésitez pas à proposer des améliorations ou de nouveaux exemples.

**Q : Où puis-je trouver de l'aide supplémentaire ?**

R :
- Consultez le [tutoriel débutant](tutorials/getting-started.md)
- Parcourez les [exemples de code](examples/)
- Consultez la [documentation DocumentCloud](https://www.documentcloud.org/help/api/)
- Contactez-nous : data@disclose.ngo


## Contact

Si vous n'avez pas trouvé l'information que vous cherchez, ou que vous avez besoin d'aide, n'hésitez pas à nous écrire à data@disclose.ngo