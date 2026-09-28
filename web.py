import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_library

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="NEGAGRI - Gestion Industrielle", page_icon="🌾", layout="wide")

# Définition des horaires d'ouverture (06:00 à 21:00)
HEURE_OUVERTURE = time(6, 0)
HEURE_FERMETURE = time(21, 0)

# --- VRAI LOGO NEGAGRI OFFICIEL INTÉGRÉ (Encodé en Base64 pour Streamlit Cloud) ---
LOGO_NEGAGRI_OFFICIEL = "data:image/png;base64,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"

# --- STYLES CSS, ANIMATIONS ET SUPPRESSIONS ---
st.markdown("""
    <style>
    /* Supprime l'en-tête, le footer et le bouton Deploy de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Animation d'apparition fluide (Fade-In) */
    @keyframes fadeIn { 
        from { opacity: 0; transform: translateY(15px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    /* Titres de la page d'accueil */
    .welcome-title { animation: fadeIn 1.2s ease-in-out; color: #0f5132; text-align: center; font-weight: bold; font-size: 3rem; margin-top: 10px; }
    .welcome-subtitle { animation: fadeIn 1.8s ease-in-out; text-align: center; color: #198754; font-size: 1.4rem; margin-bottom: 30px; }
    
    /* Boutons personnalisés aux couleurs du logo */
    .stButton>button { width: 100%; background-color: #0f5132; color: white; border-radius: 8px; font-weight: bold; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #198754; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DONNÉES EN MÉMOIRE ---
if 'stocks' not in st.session_state:
    st.session_state.stocks = {"Manioc (Kg)": 1500, "Maïs (Sacs)": 320, "Noix de Coco": 4500, "Hannetons (Bacs)": 85, "Escargots (Kilos)": 120}
if 'employes' not in st.session_state:
    st.session_state.employes = [
        {"Nom": "Bella", "Poste": "Directrice Générale", "Salaire Mensuel (FCFA)": 500000, "Code": "0000"},
        {"Nom": "Jean Mandeng", "Poste": "Chef Élevage Hannetons", "Salaire Mensuel (FCFA)": 85000, "Code": "1234"},
        {"Nom": "Marie Ngo", "Poste": "Responsable Transfo Manioc", "Salaire Mensuel (FCFA)": 90000, "Code": "5678"}
    ]
if 'eleveurs' not in st.session_state:
    st.session_state.eleveurs = [
        {"Nom/Coopérative": "Amadou Diallo", "Secteur": "Obala", "Bacs Actifs": 12, "Total Livré (Bacs)": 45},
        {"Nom/Coopérative": "Chantal Biya II", "Secteur": "Mbalmayo", "Bacs Actifs": 8, "Total Livré (Bacs)": 20}
    ]
if 'messages' not in st.session_state:
    st.session_state.messages = [{"Date": "2026-09-25", "Auteur": "Bella", "Texte": "Bienvenue sur la plateforme NEGAGRI."}]
if 'incidents' not in st.session_state:
    st.session_state.incidents = []
if 'registre_acces' not in st.session_state:
    st.session_state.registre_acces = []
if 'authentifie' not in st.session_state:
    st.session_state.authentifie = False
if 'utilisateur_actif' not in st.session_state:
    st.session_state.utilisateur_actif = None

# --- VÉRIFICATION DES HORAIRES D'OUVERTURE ---
heure_actuelle = datetime.now().time()
est_ouvert = HEURE_OUVERTURE <= heure_actuelle <= HEURE_FERMETURE

if not est_ouvert:
    st.error(f"🔒 **L'application NEGAGRI est actuellement fermée.**")
