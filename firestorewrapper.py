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
        self.user_doc = {}
        self.date_doc = {}
        self.chapter_doc = {}

    def add_user(self, DiscordID, DiscordName):
        data = {
            u'Username': u'{}'.format(DiscordName),
            u'id': u'{}'.format(DiscordID),
            u'Subjects': []
        }
        date_data_init = {
            u'id': u'{}'.format(DiscordID)
        }
        chapter_data_init = {
            u'id': u'{}'.format(DiscordID)
        }
        doc_ref = self.db.collection(u'Users').document(u'{}'.format(DiscordID))
        doc = doc_ref.get()
        if doc.exists:
            print("Document already exists!")
        else:
            print(u'No such document!')
            self.db.collection(u'Users').document(u'{}'.format(DiscordID)).set(data)
            self.db.collection(u'Chapters').document(u'{}'.format(DiscordID)).set(chapter_data_init)
            self.db.collection(u'Dates').document(u'{}'.format(DiscordID)).set(date_data_init)

    def read_user(self, DiscordID):
        user_doc_ref = self.db.collection(u'Users').document(u'{}'.format(DiscordID))
        user_doc_local = user_doc_ref.get().to_dict()
        if user_doc_local is not None:
            self.user_doc = user_doc_local
            chapter_doc_ref = self.db.collection(u'Chapters').document(u'{}'.format(DiscordID))
            date_doc_ref = self.db.collection(u'Dates').document(u'{}'.format(DiscordID))
            self.chapter_doc = chapter_doc_ref.get().to_dict()
            self.date_doc = date_doc_ref.get().to_dict()
        else:
            print("The document doesn't exist! Run add_user first!")

