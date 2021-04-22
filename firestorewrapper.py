import datetime

import firebase_admin
from decouple import config
from firebase_admin import credentials, firestore


class FirebaseAPI:
    def __init__(self):
        firebase_admin.initialize_app(credentials.Certificate(config('firebase_credentials')))
        self.db = firestore.client()
        self.subject_array = []

    def add_user(self, discord_user):
        data = {
            u'Username': u'{}'.format(discord_user.name),
            u'id': u'{}'.format(discord_user.id),
            u'Subjects': []
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
            if self.does_user_exist(discord_user) is False:
                self.add_user(discord_user)
        finally:
            user_doc = self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().to_dict()
            chapter_doc = self.db.collection(u'Chapters').document(u'{}'.format(discord_user.id)).get().to_dict()
            date_doc = self.db.collection(u'Dates').document(u'{}'.format(discord_user.id)).get().to_dict()
            return [user_doc, chapter_doc, date_doc]

    def delete_user(self, discord_user):
        if self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().exists:
            self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).delete()
        else:
            print('You cannot delete an entry that does not exist!')

    def subject_update(self, discord_user, subject):
        self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().to_dict().get("Subjects").append(
            subject)
        self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).set({
            u'Subjects': self.subject_array
        }, merge=True)

    def chapter_update(self, discord_user, chapter, subject=u'misc'):
        self.db.collection(u'Chapters').document(u'{}'.format(discord_user)).get().to_dict().get(subject).append(
            chapter)
        self.db.collection(u'Chapters').document(u'{}'.format(discord_user)).set({subject: self.subject_array},
                                                                                 merge=True)

    def date_update(self, discord_user, Subject, Input, Timestamp):
        user_doc_ref = self.db.collection(u'Dates').document(u'{}'.format(discord_user.id))
        user_doc_local = user_doc_ref.get().to_dict()
        subject_array = user_doc_local.get(u'{}'.format(Subject))
        if subject_array == 0:
            user_doc_ref.set({
                u'{}'.format(Subject): []
            }, merge=True)
            a = subject_array.append(datetime.date(Timestamp.year, Timestamp.month, Timestamp.day), Input)
            user_doc_ref.set({
                u'{}'.format(Subject): a
            }, merge=True)
        else:
            a = subject_array.append(datetime.date(Timestamp.year, Timestamp.month, Timestamp.day), Input)
            user_doc_ref.set({
                u'{}'.format(Subject): a
            }, merge=True)

    def does_user_exist(self, discord_user):
        if self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().to_dict() is None:
            return False
        else:
            return True

