# BANQUEclass Client:
    def _init_(self, nom, adresse, telephone, cnic, login, password):
        self.nom = nom
        self.adresse = adresse
        self.telephone = telephone
        self.cnic = cnic
        self.login = login
        self.password = password
        self.accounts = []

    def afficher_info(self):
        return f"Client: {self.nom}, Adresse: {self.adresse}, Tel: {self.telephone}"
