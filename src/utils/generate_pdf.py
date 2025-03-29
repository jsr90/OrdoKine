from fpdf import FPDF
import webbrowser
from datetime import datetime
import sys
import os
import json

sys.path.append("../")

from models.patient import Patient
from models.dispositif import Dispositif
from models.praticien import Praticien
from models.prescription import Prescription

def generate_pdf(prescription_id):

    prescription = Prescription.get_by_id(prescription_id)
    patient = Patient.get_by_id(prescription.data['patient_id'])
    praticien = Praticien.get_by_id(prescription.data['praticien_id'])
    dispositif_ids = prescription.data['dispositifs']
    dispositifs = [{'nom': Dispositif.get_by_id(
        d['dispositif_id']).data['nom'], 'quantity': d['quantity']}
        for d in dispositif_ids]

    class PDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 13)
            self.cell(0, 10, praticien.data['nom'].upper(
            )+' '+praticien.data['prenom'].capitalize(), align='C', ln=True)
            self.set_font('Helvetica', 'I', 11)
            self.cell(0, 8, praticien.data['profession'], align='C', ln=True)
            self.cell(
                0, 8, praticien.data['numero_professionnel'], align='C', ln=True)
            self.cell(0, 8, praticien.data['adresse']['voie'], align='C', ln=True)
            self.cell(0, 8, praticien.data['adresse']['code_postal']+' ' +
                      praticien.data['adresse']['ville'].upper(), align='C', ln=True)
            self.cell(
                0, 8, f"{praticien.data['telephone']} / {praticien.data['portable']}", align='C', ln=True)
            self.cell(0, 8, f"{praticien.data['email']}", align='C', ln=True)
            self.ln(10)

        def footer(self):
            self.set_y(-25)
            self.set_font('Helvetica', 'I', 10)
            self.cell(0, 10, praticien.data['nom'].upper(
            )+' '+praticien.data['prenom'].capitalize(), 0, 0, 'C')
            self.set_y(-20)
            self.cell(0, 10, f"Cabinet de kinésithérapie - {praticien.data['adresse']['voie']}. {praticien.data['adresse']['code_postal']}, {praticien.data['adresse']['ville']}",
                      0, 0, 'C')
            self.set_y(-15)
            self.cell(
                0, 10, f"{praticien.data['telephone']} - {praticien.data['portable']}", 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()

    # Date et lieu
    pdf.set_y(75)
    pdf.set_font('Helvetica', size=12)
    date_prescription = datetime.strptime(
        prescription.data['date_prescription'], "%Y-%m-%d").strftime('%d/%m/%Y')
    pdf.cell(
        0, 10, f"À {praticien.data['adresse']['ville']}, le {date_prescription}", ln=True, align='R')

    # Patient
    line = f"{patient.data['nom'].upper()} {patient.data['prenom'].capitalize()}"
    if patient.data.get('date_naissance'):
        date_naissance = datetime.strptime(
            patient.data['date_naissance'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y')
        line += f", né(e) le {date_naissance}"
    if patient.data.get('nir'):
        line += f" ({patient.data['nir']})"
    pdf.set_font('Helvetica', 'B', size=12)
    pdf.cell(0, 10, line, ln=True, border=0)

    # Dispositif(s)
    pdf.set_font('Helvetica', size=12)
    for dispositif in dispositifs:
        l = f"  - {dispositif['nom']}"
        l += f": {str(dispositif.get('quantity', 1))} unité(s)"
        pdf.cell(0, 10, l, ln=True, border=0)

    # Chemin pour enregistrer le fichier PDF
    file_path = f"{patient.data['nom'].upper()}_{patient.data['prenom'].capitalize()}_{prescription.id}.pdf"

    # Enregistrer le fichier PDF
    pdf.output(file_path)

    # Ouvrir le fichier PDF dans nouvel onglet du navigateur
    webbrowser.open_new_tab(file_path)

    return f"Ordonnance générée avec succès dans {file_path}."
