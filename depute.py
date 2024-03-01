import json, webbrowser, sys
from jinja2 import Template

# ce fichier s'occupe d'afficher les détails d'un député quand on clique sur un dans l'hemicycle 


def loadDeputes() :
  # charger le fichier json
  file = open('nosdeputes.json', 'r')
  data = file.read()
  obj = json.loads(data)
  deputes = obj['deputes']
  return deputes


# carte du député template
card_str = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ titre_page }}</title>
<style>
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
  }

  .card {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    max-width: 400px;
    width: 100%;
    transition: transform 0.3s ease;
  }

  .card:hover {
    transform: translateY(-10px);
  }

  .card-content {
    padding: 20px;
  }

  .card-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
  }

  .card-description {
    font-size: 16px;
    color: #666;
    margin-bottom: 20px;
  }
  li.email {
      list-style-type:none;
      font-size: 12px;
      margin: auto auto 6px 12px;  
  }
  span.bold {
      font-weight:700;
  }
</style>
</head>
<body>

<div class="card">
  <div class="card-content">
    <h2 class="card-title"><span class="bold"> {{ nom_complet }} ({{sexe}}, id: {{ id }})</span></h2>
    <p class="card-description">Date de naissance:<span class="bold"> {{ date_naissance }}</span></p>
    <p class="card-description">Lieu de naissance:<span class="bold"> {{ lieu_naissance }}</span></p>
    <p class="card-description">Parti:<span class="bold"> {{ partie }} ({{ groupe_sigle }})</span></p>
    <p class="card-description">Circonscription:<span class="bold"> {{ circonscription }}</span></p>
    <h4 class="card-subtitle">Emails:</h3>
    {% for email in emails %}
        <li class="email">{{ email.email }}</li>
    {% endfor %}
  </div>
</div>

</body>
</html>"""

template = Template(card_str)

# chercher le député 

depute_data = {}

# récupere l'id du député à partir du fichier hemicycle.py
id_depute = int(sys.argv[1])

for depute in loadDeputes():
    if depute['depute']['id'] == id_depute: # l'id du député à récupérer du lien hypertexte ?
        #formattage de date de naissance
        date_naissance = depute['depute']['date_naissance'].split("-")
        formated_date_naissance = "-".join(date_naissance[::-1])
        # données du député
        depute_data = {
            'id': id_depute,
            'titre_page': "Détails du député",
            'nom_complet': depute['depute']['nom'],
            'sexe': 'Homme' if depute['depute']['sexe'] == 'H' else 'Femme', 
            'date_naissance': formated_date_naissance,
            'lieu_naissance': depute['depute']['lieu_naissance'],
            'partie': depute['depute']['parti_ratt_financier'],
            'groupe_sigle': depute['depute']['groupe_sigle'],
            'circonscription': depute['depute']['nom_circo'],
            'emails': depute['depute']['emails']
        }
        break
    
        
if not depute_data: # vérifier si le député existe selon l'id
  print("id : " + str(id_depute))
  print('information introuvable')  
else:
  output = template.render(depute_data)
  with open('depute_details.html', 'w', encoding='utf-8') as f:
    f.write(output)
  webbrowser.open_new('depute_details.html')
  print("HTML file generated successfully!")


