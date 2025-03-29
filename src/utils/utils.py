import gradio as gr
from models.patient import Patient
from models.dispositif import Dispositif
from models.praticien import Praticien
from models.prescription import Prescription
from utils.generate_pdf import generate_pdf

def reload_dropdowns():
    """
    Recharge les listes déroulantes avec les praticiens, patients et dispositifs disponibles.
    """
    praticiens = Praticien.list_all()
    patients = Patient.list_all()
    dispositifs = Dispositif.list_all()

    return gr.Dropdown(choices=[(f"{p['nom']}", p['_id']) for p in praticiens], label="Sélectionnez un praticien"), \
        gr.Dropdown(choices=[(f"{p['nom']}, {p['prenom']}", p['_id']) for p in patients], label="Sélectionnez un patient"), \
        gr.Dropdown(choices=[(d['nom'], d['_id'])
                    for d in dispositifs], label="Sélectionnez un dispositif", multiselect=True)


def generer_prescription(praticien_id, patient_id, dispositif_ids, date_prescription):
    """
    Génère une prescription à partir des données fournies.
    """
    try:
        if not praticien_id or not patient_id or not dispositif_ids or not date_prescription:
            return "Erreur : Tous les champs doivent être remplis."

        prescription = Prescription(
            praticien_id=praticien_id,
            patient_id=patient_id,
            dispositifs=[{'dispositif_id': dispositif_id, 'quantity': 1}
                         for dispositif_id in dispositif_ids],
            date_prescription=date_prescription
        )
        prescription.create()

        generate_pdf(prescription.id)
        return f"Prescription générée avec succès : {prescription.id}"

    except Exception as e:
        return f"Erreur lors de la génération de la prescription."


def ajouter_patient(nom, prenom, date_naissance=None, nir=None):
    """
    Ajoute un nouveau patient avec les informations fournies.
    """
    try:
        if not nom or not prenom:
            return "Erreur : Les champs nom et prénom doivent être remplis."

        data = {
            "nom": nom,
            "prenom": prenom,
            "date_naissance": date_naissance,
            "nir": nir
        }
        patient = Patient(**data)
        patient.create()

        return f"Patient ajouté avec succès : {patient.id}"
    except Exception as e:
        return f"Erreur lors de l'ajout du patient."


def ajouter_dispositif(nom):
    """
    Ajoute un nouveau dispositif avec les informations fournies.
    """
    try:
        if not nom:
            return "Erreur : Tous les champs doivent être remplis."

        dispositif = Dispositif(**{
            "nom": nom
        })
        dispositif.create()

        return f"Dispositif ajouté avec succès : {dispositif.id}"

    except Exception as e:
        return f"Erreur lors de l'ajout du dispositif."
