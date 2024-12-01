import os
from datetime import datetime
import requests

def get_realtime_bicycle_data() -> None:
    """
    Récupération des données en temps réel des vélos en libre-service pour Paris, Nantes, et Toulouse.

    Cette fonction :
    1. Télécharge les données en temps réel depuis les API ouvertes des trois villes.
    2. Sauvegarde les données JSON dans des fichiers locaux spécifiques pour chaque ville.
    3. Affiche un message pour indiquer si les données ont été récupérées avec succès ou si une erreur s'est produite.

    Les fichiers sont enregistrés dans un répertoire local au format : `nom_ville_realtime_bicycle_data.json`.
    """

    # URLs des API pour les données des vélos en libre-service
    urls = [
        "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json",
        "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_stations-velos-libre-service-nantes-metropole-disponibilites/exports/json",
        "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/api-velo-toulouse-temps-reel/exports/json?lang=fr&timezone=Europe%2FParis"
    ]

    # Liste des noms de villes correspondant aux URLs
    cities = ["paris", "nantes", "toulouse"]

    for url, city in zip(urls,cities):
        response = requests.request("GET", url)
        try:
            if response.status_code == 200:
                serialize_data(response.text, city + "_realtime_bicycle_data.json")
                print(f"Les données de {city} ont été récuperées")
            else:
                print(f"Error: Impossible de récuper les données de {city} (status code: {response.status_code})")
        except requests.exceptions.RequestException as e:
            # Gestion des erreurs liées à la connexion ou à la requête
            print(f"Erreur lors de la connexion à {city} : {e}")

def get_paris_realtime_bicycle_data() -> None:
    """
    Récupère les données en temps réel des stations de vélos à Paris 
    depuis l'API OpenData Paris et les sauvegarde sous forme de fichier JSON.

    Les données sont sauvegardées dans le dossier : `data/raw_data/YYYY-MM-DD`.
    """
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json"
    
    response = requests.request("GET", url)
    
    serialize_data(response.text, "paris_realtime_bicycle_data.json")

def get_nante_realtime_bicycle_data() -> None:
    """
    Récupère les données en temps réel des stations de vélos à Nantes 
    depuis l'API Nantes Métropole et les sauvegarde sous forme de fichier JSON.

    Les données sont sauvegardées dans le dossier : `data/raw_data/YYYY-MM-DD`.
    """
    url = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_stations-velos-libre-service-nantes-metropole-disponibilites/exports/json"
    
    response = requests.request("GET", url)
    
    serialize_data(response.text, "nantes_realtime_bicycle_data.json")

def get_toulouse_realtime_bicycle_data() -> None:
    """
    Récupère les données en temps réel des stations de vélos à Toulouse 
    depuis l'API Toulouse Métropole et les sauvegarde sous forme de fichier JSON.

    Les données sont sauvegardées dans le dossier : `data/raw_data/YYYY-MM-DD`.
    """
    url = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/api-velo-toulouse-temps-reel/exports/json?lang=fr&timezone=Europe%2FParis"
    
    response = requests.request("GET", url)
    
    serialize_data(response.text, "toulouse_realtime_bicycle_data.json")

def get_commune_data() -> None:
    """
    Récupère les données des communes françaises depuis l'API GeoAPI et 
    les sauvegarde sous forme de fichier JSON.

    Les données sont sauvegardées dans le dossier : `data/raw_data/YYYY-MM-DD`.
    """
    url = "https://geo.api.gouv.fr/communes"
    
    response = requests.request("GET", url)

    if response.status_code == 200:
        serialize_data(response.text, "commune_data.json")
        print(f"Les données des communes ont été récuperées")
    else:
        print(f"Error: Impossible de récuper les données des communes (status code: {response.status_code})")

def serialize_data(raw_json: str, file_name: str) -> None:
    """
    Sauvegarde les données brutes JSON dans un fichier sous le répertoire 
    `data/raw_data/YYYY-MM-DD`.

    Args:
        raw_json (str): Les données brutes en format JSON sous forme de chaîne.
        file_name (str): Nom du fichier dans lequel les données seront sauvegardées.
    """

    today_date = datetime.now().strftime("%Y-%m-%d")
    
    if not os.path.exists(f"data/raw_data/{today_date}"):
        os.makedirs(f"data/raw_data/{today_date}")

    with open(f"data/raw_data/{today_date}/{file_name}", "w") as fd:
        fd.write(raw_json)
