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

def extract_deputies_info(xml_content):
    deputies_info = []
    root = ET.fromstring(xml_content)
    for deputy in root.findall('.//depute'):
        slug = deputy.find('slug').text
        parti_ratt_financier = deputy.find('parti_ratt_financier').text
        deputies_info.append({'slug': slug, 'parti_ratt_financier': parti_ratt_financier})
    return deputies_info

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
        if numero in range(1, 101):
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

def save_votes_to_csv(all_votes, deputies_info):
    if all_votes:
        with open('deputy_votes_new_last2.csv', 'w', newline='') as csvfile:
            fieldnames = ['deputy_name', 'parti_ratt_financier', 'numero', 'date', 'type', 'sort', 'titre', 'nombre_votants', 'nombre_pours', 'nombre_contres', 'nombre_abstentions', 'position']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for deputy_slug, votes in all_votes.items():
                deputy_info = next((d for d in deputies_info if d['slug'] == deputy_slug), None)
                if deputy_info:
                    for vote in votes:
                        writer.writerow({'deputy_name': deputy_slug, 'parti_ratt_financier': deputy_info['parti_ratt_financier'], 'position': vote['position'], **vote})
    else:
        print("Aucune donnée de député disponible.")

def main():
    # Récupérer les députés et extraire les slugs et les partis rattachés financièrement
    deputies_xml = fetch_deputies()
    if deputies_xml:
        deputies_info = extract_deputies_info(deputies_xml)

        # Récupérer les votes de chaque député et extraire les informations
        all_votes = {}
        for deputy_info in deputies_info:
            deputy_slug = deputy_info['slug']
            votes_xml = fetch_deputy_votes(deputy_slug)
            if votes_xml:
                vote_info = extract_vote_info(votes_xml)
                all_votes[deputy_slug] = vote_info

        # Sauvegarder les informations de vote extraites dans un fichier CSV
        save_votes_to_csv(all_votes, deputies_info)
    else:
        print("Aucune donnée de député disponible.")

if __name__ == "__main__":
    main()
