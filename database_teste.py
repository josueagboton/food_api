from djongo import models

db = models.get_database()

if db.connection:
    print("Connexion à la base de données réussie")
else:
    print("Échec de la connexion à la base de données")
