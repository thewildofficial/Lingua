import firebase_admin
from decouple import config
from firebase_admin import credentials, firestore

class FirebaseAPI:

    def __init__(self):
        firebase_admin.initialize_app(credentials.Certificate(config('firebase_credentials')))
        self.db = firestore.client()

    def get_information(self,DiscordUser):
        # this should return a dictionary of {subject1: [chapter1,chapter2,chaptern]}
        self.create_user(DiscordUser) #creates the user just in case. this prevents a UserNotFound error
        return self.db.collection("Chapters").document(DiscordUser.name).get().to_dict()

    def create_user(self,DiscordUser):
        # if not user.exists()
        document = self.db.collection("Chapters").document(DiscordUser.name)
        if document.get().to_dict is None:
            document.set(
                    {
                        "id": DiscordUser.id
                    }
             )
