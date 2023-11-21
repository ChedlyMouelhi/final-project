#bonjour, c'est ma version finale téléchargée, j'ai essayé de valider toutes les modifications mais pour une raison quelconque,
#cela n'a pas fonctionné, cela n'a fonctionné que pour la première version, donc voici la version finale, 
#je comprends parfaitement que je n'obtiendrai pas la note complète mais au moins Je n'obtiens pas de 0%
#j'ai même fait l'installation de requests avec python3 -m pip install requests.
import argparse
import requests
from datetime import date


def analyser_commande():
    parser = argparse.ArgumentParser(description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")
    parser.add_argument('symboles', nargs='+', help='Nom d\'un symbole boursier')
    parser.add_argument('-d', '--début', dest='début', type=str, help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
    parser.add_argument('-f', '--fin', dest='fin', type=str, help='Date recherchée la plus récente (format: AAAA-MM-JJ)')
    parser.add_argument('-v', '--valeur', dest='valeur', choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
                        default='fermeture', help='La valeur désirée (par défaut: fermeture)')
    return parser.parse_args()

def produire_historique(symbole, début, fin, valeur):
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    params = {'début': début, 'fin': fin}
    response = requests.get(url=url, params=params)

    if response.status_code == 200:
        data = response.json()
        periode = data['période']  # Correction: La variable "période" était mal écrite
        historique = data['historique']

        print(f"titre={symbole}: valeur={valeur}, début={début}, fin={fin}")
        historique_list = sorted(historique.items())
        historique_values = [(date.fromisoformat(date_str), entry[valeur]) for date_str, entry in historique_list]
        print(historique_values)
    else:
        print(f"Erreur: Impossible de récupérer l'historique pour {symbole}")

def main():
    args = analyser_commande()

    début = date.fromisoformat(args.début) if args.début else date.today() if args.début else date.today()
    fin = date.fromisoformat(args.fin) if args.fin else date.today() if args.fin else date.today()

    for symbole in args.symboles:
        produire_historique(symbole, str(début), str(fin), args.valeur)

if __name__ == "__main__":
    main()
