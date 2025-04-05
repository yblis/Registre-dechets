"""Script to initialize the database with default reference data."""
from app import create_app, db
from app.models import (WasteType, Producer, Transporter,
                       TreatmentOperation, EliminationOperation)

def init_db():
    app = create_app()
    with app.app_context():
        # Common waste types
        waste_types = [
            WasteType(code='20 03 01', description='Déchets municipaux en mélange', dangerous=False),
            WasteType(code='20 01 21', description='Tubes fluorescents et autres déchets contenant du mercure', dangerous=True),
            WasteType(code='17 05 03', description='Terres et cailloux contenant des substances dangereuses', dangerous=True),
            WasteType(code='15 01 01', description='Emballages en papier/carton', dangerous=False),
            WasteType(code='13 02 05', description='Huiles moteur, de boîte de vitesses et de lubrification non chlorées', dangerous=True)
        ]
        db.session.add_all(waste_types)

        # Treatment operations (codes R)
        treatment_operations = [
            TreatmentOperation(code='R1', description='Utilisation principale comme combustible'),
            TreatmentOperation(code='R3', description='Recyclage des matières organiques'),
            TreatmentOperation(code='R4', description='Recyclage des métaux'),
            TreatmentOperation(code='R5', description='Recyclage des matières minérales'),
            TreatmentOperation(code='R7', description='Récupération des produits servant à la captation des polluants')
        ]
        db.session.add_all(treatment_operations)

        # Elimination operations (codes D)
        elimination_operations = [
            EliminationOperation(code='D1', description='Dépôt sur ou dans le sol'),
            EliminationOperation(code='D5', description='Mise en décharge aménagée'),
            EliminationOperation(code='D8', description='Traitement biologique'),
            EliminationOperation(code='D9', description='Traitement physico-chimique'),
            EliminationOperation(code='D10', description='Incinération à terre')
        ]
        db.session.add_all(elimination_operations)

        # Example producer
        example_producer = Producer(
            name='Entreprise Example',
            siret='12345678901234',
            address='123 rue des Entreprises, 75001 Paris'
        )
        db.session.add(example_producer)

        # Example transporter
        example_transporter = Transporter(
            name='Transport Express',
            siret='98765432109876',
            address='456 avenue du Transport, 69001 Lyon',
            registration='TR123456'
        )
        db.session.add(example_transporter)

        try:
            db.session.commit()
            print("Base de données initialisée avec succès !")
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'initialisation : {str(e)}")

if __name__ == '__main__':
    init_db()
