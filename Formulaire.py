
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from sqlalchemy import text 

# Configuration de la page
st.set_page_config(
    page_title="Formulaire d'évaluation dentaire",
    page_icon="🦷",
    layout="wide"
)

def create_dental_dict():
    """Crée un dictionnaire avec toutes les dents."""
    dental_dict = {}
    
    # Quadrant supérieur droit (1)
    for i in range(11, 18):
        dental_dict[str(i)] = ""
        
    # Quadrant supérieur gauche (2)
    for i in range(21, 28):
        dental_dict[str(i)] = ""
        
    # Quadrant inférieur gauche (3)
    for i in range(31, 38):
        dental_dict[str(i)] = ""
        
    # Quadrant inférieur droit (4)
    for i in range(41, 48):
        dental_dict[str(i)] = ""
        
    return dental_dict

def main():
    st.title("🦷 Formulaire d'évaluation dentaire")
    st.markdown("---")
 


    with st.form(key="dental_form"):
        # Informations patient
        col1, col2, col3 = st.columns(3)
        with col1:
            patient_name = st.text_input(
                "Nom du patient",
                placeholder="Entrez le nom du patient"
            )
        with col2:
            patient_id = st.text_input(
                "Numéro du patient",
                placeholder="ID du patient"
            )
        with col3:
            exam_date = st.date_input("Date de l'examen", datetime.now())

        st.markdown("### État de l'éruption dentaire")
        
        # Options pour chaque dent
        dental_status_options = [
            "Sélectionner un état",
            "Absence d'éruption",
            "Éruption partielle",
            "Éruption complète"
        ]

        # Création de 4 colonnes pour les quadrants
        dental_data = create_dental_dict()
        
        # Quadrant 1 (supérieur droit)
        st.markdown("#### Quadrant 1 (Supérieur Droit)")
        cols_q1 = st.columns(7)
        for i, tooth_num in enumerate(range(11, 18)):
            with cols_q1[i]:
                dental_data[str(tooth_num)] = st.selectbox(
                    f"Dent {tooth_num}",
                    options=dental_status_options,
                    key=f"tooth_{tooth_num}"
                )

        # Quadrant 2 (supérieur gauche)
        st.markdown("#### Quadrant 2 (Supérieur Gauche)")
        cols_q2 = st.columns(7)
        for i, tooth_num in enumerate(range(21, 28)):
            with cols_q2[i]:
                dental_data[str(tooth_num)] = st.selectbox(
                    f"Dent {tooth_num}",
                    options=dental_status_options,
                    key=f"tooth_{tooth_num}"
                )

        # Quadrant 3 (inférieur gauche)
        st.markdown("#### Quadrant 3 (Inférieur Gauche)")
        cols_q3 = st.columns(7)
        for i, tooth_num in enumerate(range(31, 38)):
            with cols_q3[i]:
                dental_data[str(tooth_num)] = st.selectbox(
                    f"Dent {tooth_num}",
                    options=dental_status_options,
                    key=f"tooth_{tooth_num}"
                )

        # Quadrant 4 (inférieur droit)
        st.markdown("#### Quadrant 4 (Inférieur Droit)")
        cols_q4 = st.columns(7)
        for i, tooth_num in enumerate(range(41, 48)):
            with cols_q4[i]:
                dental_data[str(tooth_num)] = st.selectbox(
                    f"Dent {tooth_num}",
                    options=dental_status_options,
                    key=f"tooth_{tooth_num}"
                )

        # Zone de commentaires
        st.markdown("### Commentaires supplémentaires")
        comments = st.text_area(
            "",
            placeholder="Ajoutez vos observations ici...",
            height=100
        )

        # Bouton de soumission
        submitted = st.form_submit_button(
            "Enregistrer l'évaluation",
            use_container_width=True,
            type="primary"
        )

    # Traitement après la soumission
    if submitted:
        if not patient_name or not patient_id:
            st.error("⚠️ Veuillez remplir les informations du patient.", icon="⚠️")
        else:
            # Création du dictionnaire final
            final_data = {
                "patient_name": patient_name,
                "patient_id": patient_id,
                "exam_date": exam_date.strftime("%Y-%m-%d"),
                "dental_status": dental_data,
                "comments": comments
            }
            conn = st.connection('mysql', type='sql')
            with conn.session as s:
                s.execute(
                text('INSERT INTO patient(name,identifier,comment) VALUES (:name, :identifier, :comment);'),
                params=dict( name = patient_name, identifier = patient_id, comment = comments))
                s.commit()
           
            ###query = ' INSERT INTO patient (name, identifier, comment) VALUES("'+patient_name+'","'+patient_id+'","'+comments+'")'
            

           #### conn.query(query,ttl=600)
            
            
 
            # Affichage du succès
            st.success("✅ Évaluation enregistrée avec succès!", icon="✅")
            
            # Affichage du récapitulatif
            st.write("### Récapitulatif de l'évaluation")
            st.write(f"**Patient:** {patient_name} (ID: {patient_id})")
            st.write(f"**Date d'examen:** {exam_date.strftime('%d/%m/%Y')}")
            
            # Création d'un DataFrame pour afficher les résultats
            df = pd.DataFrame([dental_data]).T
            df.columns = ["État"]
            df = df[df["État"] != "Sélectionner un état"]  # Ne montrer que les dents évaluées
            
            if not df.empty:
                st.write("#### État des dents évaluées")
                st.dataframe(df)
            
            if comments:
                st.write("#### Commentaires")
                st.info(comments)

            # Option pour sauvegarder en JSON (vous pouvez adapter selon vos besoins)
            st.download_button(
                label="📥 Télécharger l'évaluation (JSON)",
                data=json.dumps(final_data, indent=4, ensure_ascii=False),
                file_name=f"evaluation_dentaire_{patient_id}_{exam_date.strftime('%Y%m%d')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()