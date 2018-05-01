import os
import json
from random import randint
from faker import Faker
from jobplus.models import db, User, Job

fake = Faker()

def iter_users():
    yield User(
            name = 'superLam',
            email = 'Lamgor@123.com',
            password = '123456',
            job = 'fishing'
            )

def iter_job():
    author = User.query.filter_by(name='superLam').first()
    with open(os.path.join(os.path.dirname(__file__),'..','datas','jobtest.json')) as f:
        jobs = json.load(f)
    for job in jobs:
        name = job['name']

