### [Disclose Data - Explorateur de données des autorités environnementales](https://data.disclose.ngo/explorateur-autorite-environnementale)

# Documentation API

- [Généralités](#généralités)
- [Champs DocumentCloud](#champs-documentcloud)
- [Métadonnées des documents](#métadonnées-des-documents)
- [Exemples de requêtes](#exemples-de-requêtes)
- [Exports CSV](#exports-csv)

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


## Contact

Si vous n'avez pas trouvé l'information que vous cherchez, ou que vous avez besoin d'aide, n'hésitez pas à nous écrire à data@disclose.ngo