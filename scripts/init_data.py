import csv
import os
from app import create_app, db
from app.models import (
    WasteType, Producer, Transporter,
    TreatmentOperation, EliminationOperation
)

def import_waste_types():
    with open('app/utils/export_templates/waste_types.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            waste_type = WasteType(
                code=row['code'],
                description=row['description'],
                dangerous=row['dangerous'].lower() == 'true'
            )
            db.session.add(waste_type)

def import_producers():
    with open('app/utils/export_templates/producers.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            producer = Producer(
                name=row['name'],
                siret=row['siret'],
                address=row.get('address', 'Adresse non spécifiée')  # Ajout d'une adresse par défaut
            )
            db.session.add(producer)

def import_transporters():
    with open('app/utils/export_templates/transporters.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transporter = Transporter(
                name=row['name'],
                siret=row['siret'],
                registration=row['registration'],
                address=row.get('address', 'Adresse non spécifiée')  # Ajout d'une adresse par défaut
            )
            db.session.add(transporter)

def import_treatment_operations():
    with open('app/utils/export_templates/treatment_operations.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            operation = TreatmentOperation(
                code=row['code'],
                description=row['description']
            )
            db.session.add(operation)

def import_elimination_operations():
    with open('app/utils/export_templates/elimination_operations.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            operation = EliminationOperation(
                code=row['code'],
                description=row['description']
            )
            db.session.add(operation)

def init_data():
    """Initialise les données de référence."""
    app = create_app()
    with app.app_context():
        # Vérifier si des données existent déjà
        if WasteType.query.first():
            print("Les données sont déjà initialisées")
            return

        try:
            import_waste_types()
            import_producers()
            import_transporters()
            import_treatment_operations()
            import_elimination_operations()
            db.session.commit()
            print("Données de référence importées avec succès")
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'importation des données: {str(e)}")

if __name__ == '__main__':
    init_data()
