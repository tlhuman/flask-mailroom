"""
database models
"""
import os

from peewee import Model, CharField, IntegerField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))

class Donor(Model):
    """Donor"""
    name = CharField(max_length=255, unique=True)

    class Meta:
        """Meta"""
        database = db

class Donation(Model):
    """Donation"""
    value = IntegerField()
    donor = ForeignKeyField(Donor, backref='donations')

    class Meta:
        """Meta"""
        database = db
