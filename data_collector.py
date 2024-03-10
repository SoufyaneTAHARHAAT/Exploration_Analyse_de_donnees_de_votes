import csv
import requests
import xml.etree.ElementTree as ET

def fetch_deputies():
    url = "https://www.nosdeputes.fr/deputes/xml"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Échec de récupération des données des députés. Code d'état : {response.status_code}")
        return None

def extract_slugs(xml_content):
    slugs = []
    root = ET.fromstring(xml_content)
    for deputy in root.findall('.//depute'):
        slug = deputy.find('slug').text
        slugs.append(slug)
    return slugs

def fetch_deputy_votes(deputy_slug):
    url = f"https://2017-2022.nosdeputes.fr/{deputy_slug}/votes/xml"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Échec de récupération des données pour le député {deputy_slug}. Code d'état : {response.status_code}")
            return None
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")

def extract_vote_info(xml_content):
    votes = []
    root = ET.fromstring(xml_content)
    for vote in root.findall('.//vote'):
        scrutin = vote.find('scrutin')
        numero = int(scrutin.find('numero').text)
        if numero in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            position = vote.find('position').text
            vote_info = {
                'numero': numero,
                'date': scrutin.find('date').text,
                'type': scrutin.find('type').text,
                'sort': scrutin.find('sort').text,
                'titre': scrutin.find('titre').text,
                'nombre_votants': int(scrutin.find('nombre_votants').text),
                'nombre_pours': int(scrutin.find('nombre_pours').text),
                'nombre_contres': int(scrutin.find('nombre_contres').text),
                'nombre_abstentions': int(scrutin.find('nombre_abstentions').text),
                'position': position
            }
            votes.append(vote_info)
    return votes


# Récupérer les députés et extraire les slugs
sum_voted = 0
sum_nonvoted = 0
sum = 0
deputies_xml = fetch_deputies()
if deputies_xml:
    deputy_slugs = extract_slugs(deputies_xml)
    # Récupérer les votes de chaque député et extraire les informations
    all_votes = {}
    for deputy_slug in deputy_slugs:
        sum +=1
        votes_xml = fetch_deputy_votes(deputy_slug)
        if votes_xml:
            vote_info = extract_vote_info(votes_xml)
            all_votes[deputy_slug] = vote_info
            sum_voted +=1
            print(f"Récupération des votes de {deputy_slug} numéro {sum_voted}")
        else:
            sum_nonvoted += 1

print(f"total : {sum}")
print(f"total votés : {sum_voted}")
print(f"total non votés : {sum_nonvoted}")

# Sauvegarder les informations de vote extraites dans un fichier CSV
if all_votes:
    with open('deputy_votes_new_last.csv', 'w', newline='') as csvfile:
        fieldnames = ['deputy_name', 'numero', 'date', 'type', 'sort', 'titre', 'nombre_votants', 'nombre_pours', 'nombre_contres', 'nombre_abstentions', 'position']  # Ajouter 'position' ici
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for deputy_slug, votes in all_votes.items():
            for vote in votes:
                writer.writerow({'deputy_name': deputy_slug, 'position': vote['position'], **vote})


    print("Données enregistrées dans deputy_votes_new_last.csv")
else:
    print("Aucune donnée de député disponible.")
