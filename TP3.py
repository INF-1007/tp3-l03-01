
"""
TP3 : Système de gestion de livres pour une bibliothèque

IMPORTANT :
- Suivre attentivement les directives dans le fichier README.md.
- Chaque partie du TP doit être réalisée à l'intérieur d'une fonction que vous devez créer.
- Vous devez ensuite appeler chacune des fonctions dans la fonction principale "main()"

"""

import csv
from datetime import datetime


##########################################################################################################
# PARTIE 1 : Création du système de gestion et ajout de la collection actuelle
##########################################################################################################

"""
Créer une fonction `charger_collection` qui permet de : 
    - Lire le fichier collection_bibliotheque.csv
    - Créer un dictionnaire nommé 'bibliotheque'
        - La cote doit être la clé principale
        - Chaque clé principale doit contenir :
            - titre
            - auteur
            - date_publication

Cette partie doit être faite dans une fonction qui s'appelle "charger_collection". 
"""

# Écrire votre code ici
def charger_collection(fichier_csv):
    bibliotheque = {}
    with open(fichier_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for ligne in reader:
            cote = ligne['cote_rangement']
            bibliotheque[cote] = {
                'titre': ligne['titre'],
                'auteur': ligne['auteur'],
                'date_publication': ligne['date_publication']
            }
    return bibliotheque












##########################################################################################################
# PARTIE 2 : Ajout d'une nouvelle collection à la bibliothèque
##########################################################################################################

"""
Exigences :
- Lire nouvelle_collection.csv
- Ajouter seulement les livres dont la cote n'existe pas déjà
- Afficher les messages demandés dans l'énoncé
- Retourner ou mettre à jour la bibliothèque

Cette partie doit être faite dans une fonction qui s'appelle "ajouter_nouvelle_collection". 
"""

# Écrire votre code ici
def ajouter_nouvelle_collection(bibliotheque, nouvelle_collection_csv):
    with open(nouvelle_collection_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for ligne in reader:
            cote = ligne['cote_rangement']
            titre = ligne['titre']
            auteur = ligne['auteur']
            
            if cote in bibliotheque:
                print(f"Le livre {cote} ---- {titre} par {auteur} ---- est déjà présent dans la bibliothèque")
            else:
                bibliotheque[cote] = {
                    'titre': titre,
                    'auteur': auteur,
                    'date_publication': ligne['date_publication']
                }
                print(f"Le livre {cote} ---- {titre} par {auteur} ---- a été ajouté avec succès")
    return bibliotheque









##########################################################################################################
# PARTIE 3 : Modification de la cote de rangement d'une sélection de livres
##########################################################################################################

"""
Exigences :
- Modifier les cotes des livres de William Shakespeare
- Exemple : S028 → WS028
- Modifier correctement les clés du dictionnaire

Cette partie doit être faite dans une fonction qui s'appelle "modifier_cote_shakespeare". 
"""

# Écrire votre code ici
def modifier_cote_shakespeare(bibliotheque):
    anciennes_cotes = list(bibliotheque.keys())
    for cote in anciennes_cotes:
        if bibliotheque[cote]['auteur'] == "William Shakespeare":
            # La cote est Sxxx, on veut WSxxx
            nouvelle_cote = "WS" + cote[1:] # Retire 'S' et ajoute 'WS'
            bibliotheque[nouvelle_cote] = bibliotheque.pop(cote)
    return bibliotheque









##########################################################################################################
# PARTIE 4 : Emprunts et retours de livres
##########################################################################################################

"""
Exigences :
- Ajouter les clés :
    - emprunt
    - date_emprunt
- Lire emprunts.csv
- Mettre à jour l'état des livres

Cette partie doit être faite dans une fonction qui s'appelle "ajouter_emprunts". 
"""

# Écrire votre code ici

def ajouter_emprunts(bibliotheque, emprunts_csv):
    
    with open(emprunts_csv, mode = 'r', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)

        emprunt = {}
        for ligne in lecteur:
            cote = ligne["cote_rangement"]
            date = ligne["date_emprunt"]
            emprunt[cote] = date

        for cote in bibliotheque:

            if cote in emprunt:
                bibliotheque[cote]["emprunt"] = "emprunté"
                bibliotheque[cote]["date_emprunt"] = emprunt[cote]
            else:
                bibliotheque[cote]["emprunt"] = "disponible"
                bibliotheque[cote]["date_emprunt"] = None

    return bibliotheque







##########################################################################################################
# PARTIE 5 : Livres en retard
##########################################################################################################

"""
Exigences :
- Ajouter les clés :
    - frais_retard
    - livre_perdu
- 30 jours autorisés
- 2$ par jour de retard (max 100$)
- Livre perdu après 365 jours
- Utiliser datetime

Cette partie doit être faite dans une fonction qui s'appelle "ajouter_retards". 
"""

# Écrire votre code ici
def calculer_retards(bibliotheque):

    today = datetime.now()

    print("\n--- Livres en retard ---")

    for cote in bibliotheque:

        livre = bibliotheque[cote]
        livre["frais_retard"] = 0
        livre["livre_perdu"] = False

        if livre.get("emprunt") == "emprunté":
            if livre.get("date_emprunt") is not None:
                date_emprunt = datetime.strptime(livre["date_emprunt"], "%Y-%m-%d")
                jours_ecoules = (today - date_emprunt).days

                if jours_ecoules > 30:
                    jours_retard = jours_ecoules - 30
                    frais = jours_retard * 2

                    if frais > 100:
                        frais = 100
                    livre["frais_retard"] = frais
                    print(cote, " - ", livre["titre"], " : ", frais, "$ de frais")

                if jours_ecoules > 365:
                    livre["livre_perdu"] = True

    return bibliotheque








##########################################################################################################
# PARTIE 6 : Sauvegarde de la bibliothèque
##########################################################################################################

"""
Exigences :
- Créer le fichier bibliotheque_mise_a_jour.csv
- Colonnes obligatoires :
    cote, titre, auteur, date_publication,
    emprunt, date_emprunt, frais_retard, livre_perdu
- Utiliser le module csv pour écrire le fichier

Cette partie doit être faite dans une fonction qui s'appelle "sauvegarder_bibliotheque". 
"""

# Écrire votre code ici
def sauvegarder_bibliotheque(bibliotheque, fichier_sortie):

    with open(fichier_sortie, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "cote",
            "titre",
            "auteur",
            "date_publication",
            "emprunt",
            "date_emprunt",
            "frais_retard",
            "livre_perdu"
        ])
        for cote in bibliotheque:
            livre = bibliotheque[cote]
            writer.writerow([
                cote,
                livre.get("titre", ""),
                livre.get("auteur", ""),
                livre.get("date_publication", ""),
                livre.get("emprunt", ""),
                livre.get("date_emprunt", ""),
                livre.get("frais_retard", 0),
                livre.get("livre_perdu", False)
            ])










##########################################################################################################
# PROGRAMME PRINCIPAL
##########################################################################################################

"""
Exigences :
- Appeler toutes vos fonctions dans le bon ordre
- Vérifier que le programme fonctionne sans erreur
- Afficher les résultats demandés
"""

# Écrire votre code ici
def main():

     # À enlever

    ############################################################
    # Partie 1 : Appel de la fonction charger_collection 
    ############################################################
    
    # Écrire votre code ici 
    bibliotheque = charger_collection("collection_bibliotheque.csv")

    ############################################################
    # Partie 2 : Appel de la fonction ajouter_nouvelle_collection
    ############################################################
    
    # Écrire votre code ici 
    bibliotheque = ajouter_nouvelle_collection(bibliotheque, "nouvelle_collection.csv")

    ############################################################
    # Partie 3 : Appel de la fonction modifier_cote_shakespeare
    ############################################################

    # Écrire votre code ici 
    bibliotheque = modifier_cote_shakespeare(bibliotheque)

    



    ############################################################
    # Partie 4 : Appel de la fonction ajouter_emprunts
    ############################################################

    # Écrire votre code ici 
    bibliotheque = ajouter_emprunts(bibliotheque,"emprunts.csv")




    ############################################################
    # Partie 5 : Appel de la fonction calculer_retards
    ############################################################

    # Écrire votre code ici 
    bibliotheque = calculer_retards(bibliotheque)

   

    ############################################################
    # Partie 6 : Appel de la fonction sauvegarder_bibliotheque
    ############################################################
    
    # Écrire votre code ici 
    
    sauvegarder_bibliotheque(bibliotheque, "bibliotheque_mise_a_jour.csv")



if __name__ == "__main__":
    main()