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

    def add_user(self, discord_user):
        data = {
            u'Username': u'{}'.format(discord_user.name),
            u'id': u'{}'.format(discord_user.id),
            u'Subjects': ["Biology", "Physics"]
        }
        date_data_init = {
            u'id': u'{}'.format(discord_user.id),
            u'misc': []
        }
        chapter_data_init = {
            u'id': u'{}'.format(discord_user.id),
            u'misc': [{u'A Modest Proposal': []}]
        }
        if self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().exists:
            print("Document already exists!")
        else:
            print(u'No such document!')
            self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).set(data)
            self.db.collection(u'Chapters').document(u'{}'.format(discord_user.id)).set(chapter_data_init)
            self.db.collection(u'Dates').document(u'{}'.format(discord_user.id)).set(date_data_init)

    def read_user(self, discord_user):
        try:
            assert self.does_user_exist(discord_user) is True
            self.add_user(discord_user)
        finally:
            self.chapter_doc = self.db.collection(u'Chapters').document(u'{}'.format(discord_user.id)).get().to_dict()
            self.date_doc = self.db.collection(u'Dates').document(u'{}'.format(discord_user.id)).get().to_dict()

    def delete_user(self, discord_user):
        if self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().exists:
            self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).delete()
        else:
            print('You cannot delete an entry that does not exist!')

    def subject_update(self, discord_user, subject):
        self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().to_dict().get("Subjects").append(subject)
        self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).set({
            u'Subjects': self.subject_array
        }, merge=True)

    def chapter_update(self, discord_user, chapter, subject=u'misc'):
        self.db.collection(u'Chapters').document(u'{}'.format(discord_user)).get().to_dict().get(subject).append(chapter)
        self.db.collection(u'Chapters').document(u'{}'.format(discord_user)).set({subject: self.subject_array}, merge=True)

    def date_update(self, discord_user, Subject, Chapter, Timestamp):
        user_doc_ref = self.db.collection(u'Dates').document(u'{}'.format(discord_user.id))
        user_doc_local = user_doc_ref.get().to_dict() # im not sure this is complete, so not gonna touch it

    def does_user_exist(self, discord_user):
        return self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get() is None if False else True

