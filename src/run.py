import gradio as gr
from datetime import datetime

# Importer les fonctions utilitaires
from utils.utils import reload_dropdowns, generer_prescription, ajouter_patient, ajouter_dispositif

# Obtenir la date d'aujourd'hui
date = datetime.now().strftime("%Y-%m-%d")

with gr.Blocks() as demo:
    with gr.Tab("Générer Prescription"):
        with gr.Row():
            with gr.Column():
                praticien_id, patient_id, dispositif_ids = reload_dropdowns()
                date = gr.DateTime(label="Sélectionner la date",
                                   include_time=False, type="string", value=date)

                b = gr.Button("Générer l'ordonnance")
                
                result_output = gr.Markdown()

            b.click(
                generer_prescription,
                inputs=[praticien_id, patient_id, dispositif_ids, date],
                outputs=[result_output]
            )

    with gr.Tab("Ajouter Patient/Dispositif"):
        with gr.Row("Ajouter un patient"):
            with gr.Column():
                nom_input = gr.Textbox(label="Nom")
                prenom_input = gr.Textbox(label="Prénom")
                date_naissance_input = gr.DateTime(
                    label="Date de Naissance", include_time=False, type="string")
                nir_input = gr.Textbox(label="NIR", value=None)
                ajout_result = gr.Markdown()
                gr.Button("Ajouter Patient").click(ajouter_patient, inputs=[
                    nom_input, prenom_input, date_naissance_input, nir_input], outputs=ajout_result).then(
                    reload_dropdowns, outputs=[praticien_id, patient_id, dispositif_ids])

            with gr.Column("Ajouter un dispositif"):
                nom_dispositif_input = gr.Textbox(label="Nom du Dispositif")
                ajout_dispositif_result = gr.Markdown()
                gr.Button("Ajouter Dispositif").click(ajouter_dispositif, inputs=[
                    nom_dispositif_input], outputs=ajout_dispositif_result).then(
                    reload_dropdowns, outputs=[praticien_id, patient_id, dispositif_ids])

if __name__ == "__main__":
    demo.launch(server_port=7860)
