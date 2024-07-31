import os
from dotenv import load_dotenv
import requests
from serpapi import GoogleSearch
import json
import pandas as pd
from tabulate import tabulate

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Fonction pour extraire le nom du produit depuis l'URL fournie
def extract_product_name(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
        start_index = page_content.find('"@type": "Product"')
        if start_index != -1:
            end_index = page_content.find('}', start_index)
            product_json_str = page_content[start_index:end_index+1]
            product_json = json.loads('{' + product_json_str + '}')
            product_name = product_json.get("name", None)
            return product_name
    return None

# Fonction pour effectuer une recherche via l'API SERP et retourner les résultats
def search_product_on_serpapi(product_name):
    api_key = os.getenv("SERPAPI_KEY")
    search = GoogleSearch({
        "q": product_name,
        "location": "Paris,Paris,Ile-de-France,France",
        "google_domain": "google.fr",
        "hl": "fr",
        "gl": "fr",
        "device": "desktop",
        "api_key": api_key
    })
    return search.get_dict()

# Fonction pour extraire les questions/réponses, les prix et les évaluations des résultats SERP
def extract_serp_info(serp_results):
    related_questions = serp_results.get("related_questions", [])
    prices = []
    ratings = []
    reviews_count = 0

    for item in serp_results.get("shopping_results", []):
        price = item.get("price")
        if price:
            prices.append(float(price.replace('€', '').replace(',', '.')))
        
        rating = item.get("rating")
        reviews = item.get("reviews")
        if rating and reviews:
            ratings.append((float(rating), int(reviews)))
            reviews_count += int(reviews)

    return related_questions, prices, ratings, reviews_count

# Fonction pour calculer la moyenne des prix et la note globale
def calculate_averages(prices, ratings, reviews_count):
    avg_price = sum(prices) / len(prices) if prices else 0
    total_rating = sum(rating * count for rating, count in ratings)
    avg_rating = total_rating / reviews_count if reviews_count else 0
    return avg_price, avg_rating

# Fonction pour sauvegarder les résultats SERP dans un fichier JSON
def save_serp_results(serp_results, filename):
    with open(filename, 'w') as f:
        json.dump(serp_results, f, indent=4)

# Fonction pour afficher les résultats sous forme de tableau
def print_serp_info_as_table(related_questions, prices, avg_price, avg_rating, reviews_count):
    questions_data = [(i+1, q['question'], q.get('snippet', 'No snippet available')) for i, q in enumerate(related_questions[:4])]
    questions_df = pd.DataFrame(questions_data, columns=["Q/A", "Question", "Snippet"])
    
    print(tabulate(questions_df, headers='keys', tablefmt='psql'))
    print("\nAverage Price: {:.2f}€".format(avg_price))
    print("Average Rating: {:.2f} based on {} reviews".format(avg_rating, reviews_count))

if __name__ == "__main__":
    url = "https://www.modesdemploi.fr/delonghi/magnifica-evo-ecam29061b/caracteristiques"

    # Extraction du nom du produit
    product_name = extract_product_name(url)
    if product_name:
        print(f"Product Name: {product_name}")

        # Recherche du produit sur SERP
        serp_results = search_product_on_serpapi(product_name)

        # Sauvegarde des résultats SERP dans un fichier JSON
        save_serp_results(serp_results, "serp_results.json")

        # Extraction des informations SERP
        related_questions, prices, ratings, reviews_count = extract_serp_info(serp_results)

        # Calcul des moyennes
        avg_price, avg_rating = calculate_averages(prices, ratings, reviews_count)

        # Affichage des informations sous forme de tableau
        print_serp_info_as_table(related_questions, prices, avg_price, avg_rating, reviews_count)
    else:
        print("Product name not found.")
