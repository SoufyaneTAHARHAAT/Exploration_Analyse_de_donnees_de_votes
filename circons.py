import json, webbrowser, sys
from jinja2 import Template

# ce fichier concerne la carte de france
# quand on clique sur un département, on affiche les ciconscription qui se trouvent dans ce département 


def loadDeputes() :
  # charger le fichier json
  file = open('nosdeputes.json', 'r')
  data = file.read()
  obj = json.loads(data)
  deputes = obj['deputes']
  return deputes

circons_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Circonscriptions d'un département</title>
    <style>
        * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: sans-serif;
        }
        body {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 100vh;
        background: #f6f6f6;
        }
        .box {
        width: 500px;
        margin: 20px auto;
        border-bottom: 20px solid #03a9f4;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
        }
        .box h2 {
        color: #fff;
        background: #03a9f4;
        padding: 10px 20px;
        font-size: 20px;
        font-weight: 700;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        }
        .box ul {
        position: relative;
        background: #fff;
        }
        .box ul:hover li {
        opacity: 0.2;
        }
        .box ul li {
        list-style: none;
        padding: 10px;
        width: 100%;
        background: #fff;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);
        transition: transform 0.5s;
        }
        .box ul li:hover {
        transform: scale(1.1);
        z-index: 5;
        background: #25bcff;
        box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
        color: #fff;
        opacity: 1;
        }
        .box ul li span {
        padding: 15px;
        text-align: center;
        background: #25bcff;
        color: #fff;
        display: inline-block;
        border-radius: 2px;
        font-size: 12px;
        font-weight: 600;
        transform: translateY(-2px);
        }
        .box ul li:hover span {
        background: #fff;
        color: #25bcff;
        }
    </style>
</head>
<body>
    {% for depute in circons_data %}
        <div class="box">
            <h2>Code circonscription: {{ depute.code_circo }}</h2>
            <ul>
                <li>Département: <span>{{ depute.circonscription }}</span></li>
                <li>Député: <span>{{ depute.nom_complet }}</span></li>
                <li>Lieu de naissance: <span>{{ depute.lieu_naissance }}</span></li>
                <li>Début mandat: <span>{{ depute.mandat_debut }}</span></li>                
                <li>Parti: <span>{{ depute.parti }} ({{ depute.groupe_sigle }})</span></li>
            </ul>
        </div>
    {% endfor %}
</body>
</html>

"""

template = Template(circons_str)


# chercher le député 
circons_data = []

# récupere l'id  du département 
id_departement = sys.argv[1]

for depute in loadDeputes():
    if depute['depute']['num_deptmt'] == id_departement:
        mandat_debut = depute['depute']['mandat_debut'].split("-")
        formated_mandat_debut = "-".join(mandat_debut[::-1])
        depute_data = {
            'code_circo': depute['depute']['num_circo'],
            'nom_complet': depute['depute']['nom'],
            'sexe': 'Homme' if depute['depute']['sexe'] == 'H' else 'Femme', 
            'lieu_naissance': depute['depute']['lieu_naissance'],
            'mandat_debut': formated_mandat_debut,
            'parti': depute['depute']['parti_ratt_financier'],
            'groupe_sigle': depute['depute']['groupe_sigle'],
            'circonscription': depute['depute']['nom_circo'],
        }
        circons_data.append(depute_data)
if len(circons_data) == 0:
    print("Aucune circonscription")
else:
  output = template.render(circons_data=circons_data)
  with open('circons_details.html', 'w', encoding='utf-8') as f:
    f.write(output)
  webbrowser.open_new('circons_details.html')
  print("HTML file generated successfully!")    
