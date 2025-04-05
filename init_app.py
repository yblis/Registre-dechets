from app import create_app, db
from app.models import User, WasteType, Producer, Transporter, TreatmentOperation, EliminationOperation

def init_app():
    app = create_app()
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Add default admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin')
            db.session.add(admin)
        
        # Add example waste types
        waste_types = [
            WasteType(code='20 03 01', description='Déchets municipaux en mélange', dangerous=False),
            WasteType(code='20 01 21', description='Tubes fluorescents', dangerous=True),
        ]
        for wt in waste_types:
            if not WasteType.query.filter_by(code=wt.code).first():
                db.session.add(wt)
        
        # Add example treatment operations
        treatments = [
            TreatmentOperation(code='R1', description='Utilisation comme combustible'),
            TreatmentOperation(code='R3', description='Recyclage matières organiques'),
        ]
        for t in treatments:
            if not TreatmentOperation.query.filter_by(code=t.code).first():
                db.session.add(t)
        
        # Add example elimination operations
        eliminations = [
            EliminationOperation(code='D1', description='Dépôt sur ou dans le sol'),
            EliminationOperation(code='D10', description='Incinération à terre'),
        ]
        for e in eliminations:
            if not EliminationOperation.query.filter_by(code=e.code).first():
                db.session.add(e)
        
        # Add example producer
        if not Producer.query.filter_by(siret='12345678901234').first():
            producer = Producer(
                name='Entreprise Example',
                siret='12345678901234',
                address='123 rue des Entreprises, 75001 Paris'
            )
            db.session.add(producer)
        
        # Add example transporter
        if not Transporter.query.filter_by(siret='98765432109876').first():
            transporter = Transporter(
                name='Transport Express',
                siret='98765432109876',
                address='456 avenue du Transport, 69001 Lyon',
                registration='TR123456'
            )
            db.session.add(transporter)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Base de données initialisée avec succès !")
            print("Identifiants par défaut : admin/admin")
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'initialisation : {str(e)}")

if __name__ == '__main__':
    init_app()
