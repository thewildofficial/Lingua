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
        self.subject_array = []

    def add_user(self, DiscordID, DiscordName):
        data = {
            u'Username': u'{}'.format(DiscordName),
            u'id': u'{}'.format(DiscordID),
            u'Subjects': ["Biology", "Physics"]
        }
        date_data_init = {
            u'id': u'{}'.format(DiscordID),
            u'misc': []
        }
        chapter_data_init = {
            u'id': u'{}'.format(DiscordID),
            u'misc': [{u'A Modest Proposal': []}]
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

    def delete_user(self, DiscordID):
        doc_ref = self.db.collection(u'Users').document(u'{}'.format(DiscordID))
        doc = doc_ref.get()
        if doc.exists:
            self.db.collection(u'Users').document(u'{}'.format(DiscordID)).delete()
            self.db.collection(u'Users').document(u'{}'.format(DiscordID)).delete()
            self.db.collection(u'Users').document(u'{}'.format(DiscordID)).delete()
        else:
            print('You cannot delete an entry that does not exist!')

    def subject_update(self, DiscordID, Subject_to_add):
        user_doc_ref = self.db.collection(u'Users').document(u'{}'.format(DiscordID))
        user_doc_local = user_doc_ref.get().to_dict()
        self.subject_array = user_doc_local.get("Subjects")
        self.subject_array.append(Subject_to_add)
        user_doc_ref.set({
            u'Subjects': self.subject_array
        }, merge=True)

    def chapter_update(self, DiscordID, Chapter_to_add, Subject_to_add=u'misc'):
        user_doc_ref = self.db.collection(u'Chapters').document(u'{}'.format(DiscordID))
        user_doc_local = user_doc_ref.get().to_dict()
        subject_array = user_doc_local.get(Subject_to_add)
        subject_array.append(Chapter_to_add)
        user_doc_ref.set({
            Subject_to_add: subject_array
        }, merge=True)

    def date_update(self, DiscordID, Subject, Chapter, Timestamp):
        user_doc_ref = self.db.collection(u'Dates').document(u'{}'.format(DiscordID))
        user_doc_local = user_doc_ref.get().to_dict()

