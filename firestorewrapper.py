import datetime

import firebase_admin
from decouple import config
from firebase_admin import credentials, firestore

from bot import BotInformation


class FirebaseAPI:
    def __init__(self):
        firebase_admin.initialize_app(credentials.Certificate(BotInformation.firebase_credentials))
        self.db = firestore.client()

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
            u'misc': [{u'': []}]
        }

        self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).set(data)
        self.db.collection(u'Chapters').document(u'{}'.format(discord_user.id)).set(chapter_data_init)
        self.db.collection(u'Dates').document(u'{}'.format(discord_user.id)).set(date_data_init)

    def read_user(self, discord_user, type):
        try:
            if self.does_user_exist(discord_user) is False:
                self.add_user(discord_user)
        finally:
            if type == "user":
                return self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().to_dict()
            elif type == "chapter":
                return self.db.collection(u'Chapters').document(u'{}'.format(discord_user.id)).get().to_dict()
            elif type == "date":
                return self.db.collection(u'Dates').document(u'{}'.format(discord_user.id)).get().to_dict()

    def delete_user(self, discord_user):
        if self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().exists:
            self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).delete()
        else:
            print('You cannot delete an entry that does not exist!')

    def subject_update(self, discord_user, subject):
        subjects = self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).get().to_dict().get("Subjects")
        subjects.append(subject)
        self.db.collection(u'Users').document(u'{}'.format(discord_user.id)).set({
            u'Subjects': subjects
        }, merge=True)

    def chapter_update(self, discord_user, chapter, subject=u'misc'):
        subjects = self.db.collection(u'Chapters').document(u'{}'.format(discord_user)).get().to_dict().get(subject)
        subjects.append(chapter)
        self.db.collection(u'Chapters').document(u'{}'.format(discord_user)).set({subject: subjects},
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
