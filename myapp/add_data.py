# add_data.py

from myapp.models import Test

# Ajoutez des données à la table
data_to_add = [
    {"name": "Première entrée"},
    {"name": "Deuxième entrée"},
    {"name": "Troisième entrée"},
]

for data in data_to_add:
    Test.objects.create(**data)
