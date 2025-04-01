import random
import re

class Client:
    def __init__(self, nom, adresse, telephone, cnic, login, mot_de_passe, limite_retrait):
        self.nom = nom
        self.adresse = adresse
        self.telephone = telephone
        self.cnic = cnic
        self.login = login
        self.mot_de_passe = mot_de_passe
        self.limite_retrait = limite_retrait
        self.compte = None  # Initialement, le client n'a pas de compte

    def verifier_information(self):
        """Vérifie que les informations du client sont valides."""
        if not self.verifier_nom():
            return False, "Nom invalide"
        if not self.verifier_telephone():
            return False, "Numéro de téléphone invalide"
        if not self.verifier_cnic():
            return False, "CNIC invalide"
        if not self.verifier_limite_retrait():
            return False, "Limite de retrait invalide"
        return True, "Informations valides"
    
    def verifier_nom(self):
        """Vérifie que le nom est valide (alphanumérique et d'au moins 3 caractères)."""
        return len(self.nom) >= 3
    
    def verifier_telephone(self):
        """Vérifie que le numéro de téléphone est au format valide."""
        return bool(re.match(r"^\+?[1-9]\d{1,14}$", self.telephone))  # Format international
    
    def verifier_cnic(self):
        """Vérifie que le CNIC est valide (un numéro de 13 chiffres)."""
        return bool(re.match(r"^\d{13}$", self.cnic))
    
    def verifier_limite_retrait(self):
        """Vérifie que la limite de retrait est valide (positive et raisonnable)."""
        return self.limite_retrait > 0 and self.limite_retrait <= 100000  # Exemple de limite maximale

    def creer_compte(self):
        """Crée un compte bancaire pour le client si les informations sont valides."""
        est_valide, message = self.verifier_information()
        if not est_valide:
            return message
        
        self.compte = CompteBancaire(self)
        return "Compte créé avec succès, numéro de carte attribué."

class CompteBancaire:
    def __init__(self, client):
        self.client = client
        self.numero_carte = self.generer_numero_carte()
        self.pin = None
        self.type_compte = self.attribuer_type_compte()
    
    def generer_numero_carte(self):
        """Génère un numéro de carte à 16 chiffres."""
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])
    
    def attribuer_type_compte(self):
        """Attribue un type de compte en fonction de la limite de retrait."""
        if self.client.limite_retrait <= 50000:
            return "Compte épargne"
        elif self.client.limite_retrait <= 100000:
            return "Compte courant"
        else:
            return "Compte premium"
    
    def entrer_pin(self, pin):
        """Permet au client d'entrer un numéro PIN pour son compte."""
        if len(pin) == 4 and pin.isdigit():
            self.pin = pin
            return "PIN enregistré avec succès."
        else:
            return "Le PIN doit être composé de 4 chiffres."

def inscription_utilisateur():
    """Permet à l'utilisateur de s'inscrire en fournissant ses informations."""
    print("Bienvenue dans le système d'inscription bancaire!")
    
    # Demande des informations à l'utilisateur
    nom = input("Entrez votre nom complet: ")
    adresse = input("Entrez votre adresse: ")
    telephone = input("Entrez votre numéro de téléphone: ")
    cnic = input("Entrez votre CNIC (13 chiffres): ")
    login = input("Entrez votre login: ")
    mot_de_passe = input("Entrez votre mot de passe: ")
    limite_retrait = float(input("Entrez votre limite quotidienne estimée de retrait: "))
    
    # Création de l'objet Client
    client = Client(nom, adresse, telephone, cnic, login, mot_de_passe, limite_retrait)
    
    # Vérification des informations et création du compte
    message = client.creer_compte()
    print(message)
    
    if client.compte:
        # Si le compte est créé, on demande à l'utilisateur d'entrer un PIN
        pin = input("Entrez un numéro PIN à 4 chiffres: ")
        pin_message = client.compte.entrer_pin(pin)
        print(pin_message)
        
        # Affichage des informations du compte
        print(f"Numéro de carte : {client.compte.numero_carte}")
        print(f"Type de compte : {client.compte.type_compte}")

# Appel de la fonction d'inscription
inscription_utilisateur()
