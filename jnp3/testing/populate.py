import sys
import os
import random
import lipsum

g = lipsum.Generator()

sys.path.append("/home/jnp/repo")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jnp3.settings")

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test.client import Client

for i in range(100):
    c = Client()
    cl = 'test' + str(i)

    print cl

    c.post('/register', {'username' : cl, 'password' : cl, 'password2' : cl})

    c.login(username=cl, password=cl)

    for i in range(random.randint(5, 10)):
        p = random.randint(0, 9)
        f = open("./pics/{0}.jpg".format(p), "r")
        desc = g.generate_paragraph()
        c.post('/upload', {'photo' : f, 'desc' : desc})
