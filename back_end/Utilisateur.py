import getpass

class Utilisateur:
    def __init__(self):
        self.id_utilisateur = self.get_user_id()
       
   
    @classmethod
    def get_user_id(cls):
        return getpass.getuser()
   
    def __str__(self):
        return f"Utilisateur(id='{self.id_utilisateur}')"
