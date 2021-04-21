import firebase_admin
from decouple import config
from firebase_admin import credentials, firestore

import firebase_admin
from decouple import config
from firebase_admin import credentials, firestore


class FirebaseAPI:
    def __init__(self):
        firebase_admin.initialize_app(credentials.Certificate(config('firebase_credentials')))
        self.db = firestore.client()

    def add_user(self, discord_user):
        data = {
            u'Username': u'{}'.format(discord_user.name),
            u'id': u'{}'.format(discord_user.id),
            u'Subjects': []
        }
        date_data_init = {
            u'id': u'{}'.format(discord_user.id)
        }
        chapter_data_init = {
            u'id': u'{}'.format(discord_user.id)
        }
        if self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().exists:
            raise Exception("User already exists!")
        else:
            self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).set(data)
            self.db.collection(u'Chapters').document(u'{}'.format(discord_user.id)).set(chapter_data_init)
            self.db.collection(u'Dates').document(u'{}'.format(discord_user.id)).set(date_data_init)

    def read_user(self, discord_user, type):  # getter can be chapter,dates or user_information
        try:
            # exceptions arent good in this case,we want to make the user behind the scenes,and return information instantly
            assert self.does_user_exist(discord_user) is True
            self.add_user(discord_user)
        finally:
            if type.lower() == "user_information":
                return self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().to_dict()
            elif type.lower() == "chapter":
                return self.db.collection(u'Chapters').document(u'{}'.format(discord_user.id)).get().to_dict()
            elif type.lower() == "dates":
                return self.db.collection(u'Dates').document(u'{}'.format(discord_user.id)).to_dict()

    def purge_user(self, discord_user):
        if self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).doc_ref.get().exists:
            self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).delete()
        else:
            raise Exception('You cannot delete entries that do not exist!')

    def does_user_exist(self, discord_user):  # checks if the user exists
        return self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get() is None if False else True
        # returns False if user does not exists in the database,else True
