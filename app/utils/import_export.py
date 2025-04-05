import csv
import io
from typing import List, Dict, Any, Type
import openpyxl
from flask import send_file
from werkzeug.datastructures import FileStorage
from app import db
from app.models import WasteType, Producer, Transporter, TreatmentOperation, EliminationOperation

class ImportExportManager:
    MODELS = {
        'waste_types': WasteType,
        'producers': Producer,
        'transporters': Transporter,
        'treatment_operations': TreatmentOperation,
        'elimination_operations': EliminationOperation
    }

    TEMPLATES_DIR = 'app/utils/export_templates'

    @classmethod
    def get_template(cls, entity_type: str) -> io.BytesIO:
        """Récupère le modèle d'import pour un type d'entité."""
        template_path = f"{cls.TEMPLATES_DIR}/{entity_type}.csv"
        with open(template_path, 'r', encoding='utf-8') as f:
            output = io.BytesIO()
            output.write(f.read().encode('utf-8'))
            output.seek(0)
            return output

    @classmethod
    def export_data(cls, entity_type: str) -> io.BytesIO:
        """Exporte les données d'une entité en format CSV."""
        model = cls.MODELS.get(entity_type)
        if not model:
            raise ValueError(f"Type d'entité non supporté: {entity_type}")

        data = model.query.all()
        if not data:
            return cls.get_template(entity_type)

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        # Écrire les en-têtes
        headers = [column.name for column in model.__table__.columns 
                  if column.name not in ['id', 'created_at', 'updated_at']]
        writer.writerow(headers)

        # Écrire les données
        for item in data:
            row = []
            for header in headers:
                value = getattr(item, header)
                # Convertir les booléens en 'true'/'false'
                if isinstance(value, bool):
                    value = str(value).lower()
                row.append(value)
            writer.writerow(row)

        return io.BytesIO(output.getvalue().encode('utf-8'))

    @classmethod
    def import_data(cls, entity_type: str, file: FileStorage) -> Dict[str, Any]:
        """Importe les données depuis un fichier CSV."""
        model = cls.MODELS.get(entity_type)
        if not model:
            raise ValueError(f"Type d'entité non supporté: {entity_type}")

        # Lire le fichier CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)

        # Vérifier les colonnes requises
        expected_columns = [column.name for column in model.__table__.columns 
                          if column.name not in ['id', 'created_at', 'updated_at']]
        file_columns = reader.fieldnames if reader.fieldnames else []
        missing_columns = set(expected_columns) - set(file_columns)
        if missing_columns:
            raise ValueError(f"Colonnes manquantes: {', '.join(missing_columns)}")

        # Compter les lignes
        lines = list(reader)
        stream.seek(0)
        reader = csv.DictReader(stream)
        
        results = {
            'total': len(lines),
            'created': 0,
            'updated': 0,
            'errors': []
        }

        db.session.begin_nested()  # Créer un savepoint
        
        # Traiter chaque ligne
        for row in reader:
            try:
                with db.session.no_autoflush:  # Désactiver l'autoflush
                    # Convertir les données
                    data = {}
                    for key, value in row.items():
                        if key == 'dangerous':
                            # Convertir 'true'/'false' en bool
                            data[key] = value.lower() == 'true'
                        else:
                            data[key] = value
                    
                    # Rechercher l'instance existante
                    if entity_type == 'waste_types':
                        instance = model.query.filter_by(code=data['code']).first()
                    elif entity_type == 'transporters':
                        instance = model.query.filter_by(registration=data['registration']).first()
                    elif entity_type in ['producers']:
                        instance = model.query.filter_by(siret=data['siret']).first()
                    else:
                        instance = model.query.filter_by(code=data['code']).first()
                    
                    if instance:
                        # Mettre à jour l'instance existante
                        for key, value in data.items():
                            setattr(instance, key, value)
                        results['updated'] += 1
                    else:
                        # Créer une nouvelle instance
                        instance = model(**data)
                        db.session.add(instance)
                        results['created'] += 1
                    
                    # Commit partiel après chaque ligne réussie
                    db.session.flush()

            except Exception as e:
                db.session.rollback()  # Rollback au dernier savepoint
                results['errors'].append(f"Ligne {results['created'] + results['updated'] + 2}: {str(e)}")
                continue

        # Commit final si pas d'erreurs
        try:
            if not results['errors']:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            results['errors'].append(f"Erreur lors du commit final: {str(e)}")

        return results

    @classmethod
    def export_excel(cls, entity_type: str) -> io.BytesIO:
        """Export des données au format Excel."""
        model = cls.MODELS.get(entity_type)
        if not model:
            raise ValueError(f"Type d'entité non supporté: {entity_type}")

        # Créer un nouveau classeur Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data"

        # Récupérer les en-têtes
        headers = [column.name for column in model.__table__.columns 
                  if column.name not in ['id', 'created_at', 'updated_at']]
        ws.append(headers)

        # Ajouter les données
        data = model.query.all()
        for item in data:
            row = []
            for header in headers:
                value = getattr(item, header)
                # Convertir les booléens en 'true'/'false' pour Excel
                if isinstance(value, bool):
                    value = str(value).lower()
                row.append(value)
            ws.append(row)

        # Ajuster la largeur des colonnes
        for column in ws.columns:
            max_length = 0
            column = list(column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        # Sauvegarder dans un buffer
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return output
