import random
import re

# Classe Client pour les utilisateurs individuels
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

# Classe CompteBancaire pour gérer les opérations des clients
class CompteBancaire:
    def __init__(self, client):
        self.client = client
        self.solde = 0  # Solde initial du compte
        self.numero_carte = self.generer_numero_carte()
        self.pin = None
        self.type_compte = self.attribuer_type_compte()
        self.historique_transactions = []  # Liste pour enregistrer l'historique des transactions
        self.est_gelé = False  # Indicateur pour savoir si le compte est gelé ou non
    
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
    
    def deposer_fonds(self, montant):
        """Permet au client de déposer des fonds dans son compte."""
        if self.est_gelé:
            return "Le compte est gelé, vous ne pouvez pas effectuer de dépôt."
        if montant <= 0:
            return "Le montant du dépôt doit être positif."
        self.solde += montant
        self.historique_transactions.append(f"Dépôt de {montant}€")
        return f"{montant}€ déposés avec succès."

    def retirer_fonds(self, montant):
        """Permet au client de retirer des fonds de son compte."""
        if self.est_gelé:
            return "Le compte est gelé, vous ne pouvez pas effectuer de retrait."
        if montant <= 0:
            return "Le montant du retrait doit être positif."
        if montant > self.solde:
            return "Fonds insuffisants."
        self.solde -= montant
        self.historique_transactions.append(f"Retrait de {montant}€")
        return f"{montant}€ retirés avec succès."

    def consulter_solde(self):
        """Affiche le solde actuel du compte."""
        return f"Solde actuel : {self.solde}€"
    
    def consulter_historique(self):
        """Affiche l'historique des transactions."""
        if not self.historique_transactions:
            return "Aucune transaction enregistrée."
        return "\n".join(self.historique_transactions)
    
    def transferer_fonds(self, montant, compte_destinataire):
        """Permet de transférer des fonds vers un autre compte."""
        if self.est_gelé:
            return "Le compte est gelé, vous ne pouvez pas effectuer de transfert."
        if montant <= 0:
            return "Le montant du transfert doit être positif."
        if montant > self.solde:
            return "Fonds insuffisants pour le transfert."
        self.solde -= montant
        compte_destinataire.solde += montant
        self.historique_transactions.append(f"Transfert de {montant}€ vers le compte {compte_destinataire.numero_carte}")
        compte_destinataire.historique_transactions.append(f"Réception de {montant}€ du compte {self.numero_carte}")
        return f"{montant}€ transférés avec succès vers le compte {compte_destinataire.numero_carte}."
    
    def geler_compte(self):
        """Gèle le compte pour empêcher toute opération."""
        self.est_gelé = True
        return "Compte gelé avec succès."
    
    def debloquer_compte(self):
        """Débloque un compte gelé."""
        self.est_gelé = False
        return "Compte débloqué avec succès."

# Classe EmployeBancaire pour gérer les actions des employés bancaires
class EmployeBancaire:
    def __init__(self, nom_utilisateur, mot_de_passe):
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
    
    def se_connecter(self, utilisateur, mot_de_passe):
        """Permet à l'employé de se connecter au système."""
        if self.nom_utilisateur == utilisateur and self.mot_de_passe == mot_de_passe:
            return True
        return False
    
    def consulter_comptes_clients(self, clients):
        """Affiche la liste de tous les comptes clients."""
        return [client.compte.numero_carte for client in clients if client.compte]
    
    def approuver_demande_compte(self, client):
        """Approuve la demande de création de compte du client."""
        if client.compte:
            return "Le compte est déjà créé."
        client.creer_compte()
        return "Demande de compte approuvée."
    
    def rejeter_demande_compte(self, client):
        """Rejette la demande de création de compte du client."""
        return "Demande de compte rejetée."
    
    def approuver_demande_pret(self, entreprise):
        """Approuve la demande de prêt de l'entreprise."""
        return f"Demande de prêt pour l'entreprise {entreprise.nom_entreprise} approuvée."
    
    def rejeter_demande_pret(self, entreprise):
        """Rejette la demande de prêt de l'entreprise."""
        return f"Demande de prêt pour l'entreprise {entreprise.nom_entreprise} rejetée."
    
