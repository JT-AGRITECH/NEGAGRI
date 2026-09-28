import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_library

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="NEGAGRI - Gestion Industrielle", page_icon="🌾", layout="wide")

# Définition des horaires d'ouverture (06:00 à 21:00)
HEURE_OUVERTURE = time(6, 0)
HEURE_FERMETURE = time(21, 0)

# --- TRUE LOGO NEGAGRI OFFICIAL EMBEDDED (Base64 High-Resolution String) ---
LOGO_NEGAGRI_REAL = "data:image/png;base64,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"

# --- BASES DE DONNÉES TEMPORAIRES EN MÉMOIRE ---
if 'stocks' not in st.session_state:
    st.session_state.stocks = {"Manioc (Kg)": 1500, "Maïs (Sacs)": 320, "Noix de Coco": 4500, "Hannetons (Bacs)": 85, "Escargots (Kilos)": 120}
if 'employes' not in st.session_state:
    st.session_state.employes = [
        {"Nom": "Bella", "Poste": "Directrice Générale", "Salaire (FCFA)": 500000, "Code": "0000"},
        {"Nom": "Jean Mandeng", "Poste": "Chef Élevage Hannetons", "Salaire (FCFA)": 85000, "Code": "1234"},
        {"Nom": "Marie Ngo", "Poste": "Responsable Transfo Manioc", "Salaire (FCFA)": 90000, "Code": "5678"}
    ]
if 'eleveurs' not in st.session_state:
    st.session_state.eleveurs = [
        {"Nom/Coopérative": "Amadou Diallo", "Secteur": "Obala", "Bacs Actifs": 12, "Total Livré (Bacs)": 45},
        {"Nom/Coopérative": "Chantal Biya II", "Secteur": "Mbalmayo", "Bacs Actifs": 8, "Total Livré (Bacs)": 20}
    ]
if 'ventes' not in st.session_state:
    st.session_state.ventes = [
        {"Date": "2026-09-26", "Client": "Coopérative Centre", "Produit": "Manioc (Kg)", "Quantité": 500, "Total (FCFA)": 150000}
    ]
if 'messages' not in st.session_state:
    st.session_state.messages = [{"Date": "2026-09-25", "Auteur": "Bella", "Texte": "Lancement officiel de la plateforme industrielle."}]
if 'incidents' not in st.session_state:
    st.session_state.incidents = [{"Date": "2026-09-27", "Type": "Coupure Électricité", "Secteur": "Hangar Hannetons", "Gravité": "Moyenne"}]
if 'registre_acces' not in st.session_state:
    st.session_state.registre_acces = []
if 'authentifie' not in st.session_state:
    st.session_state.authentifie = False
if 'utilisateur_actif' not in st.session_state:
    st.session_state.utilisateur_actif = None

# --- STYLES CSS PERSONNALISÉS (Thème Vert Agricole) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display:none;}
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .welcome-title { animation: fadeIn 1.2s ease-in-out; color: #005c2d; text-align: center; font-weight: bold; font-size: 3rem; margin-top: 10px; }
    .welcome-subtitle { animation: fadeIn 1.6s ease-in-out; text-align: center; color: #7cb342; font-size: 1.3rem; margin-bottom: 30px; }
    .stButton>button { width: 100%; background-color: #005c2d; color: white; border-radius: 8px; font-weight: bold; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #198754; color: white; }
    .card { padding: 25px; background-color: white; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); margin-bottom: 20px; border-left: 5px solid #005c2d; }
    h1, h2, h3 { color: #005c2d; }
    </style>
""", unsafe_allow_html=True)

# --- VÉRIFICATION HORAIRE DE SÉCURITÉ ---
heure_actuelle = datetime.now().time()
if not (HEURE_OUVERTURE <= heure_actuelle <= HEURE_FERMETURE):
    st.error(f"🔒 **L'application NEGAGRI est fermée.** Accessibilité de {HEURE_OUVERTURE.strftime('%H:%M')} à {HEURE_FERMETURE.strftime('%H:%M')}.")
    st.stop()

# --- FORMULAIRE DE CONNEXION ---
if not st.session_state.authentifie:
    st.markdown('<div class="welcome-title">NEGAGRI</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Nouvelle Génération Africaine de l\'Agriculture</div>', unsafe_allow_html=True)
    
    col_v1, col_c, col_v2 = st.columns([1, 1.4, 1])
    with col_c:
        st.image(LOGO_NEGAGRI_REAL, use_container_width=True)
        st.subheader("🔑 Authentification")
        code_saisi = st.text_input("Code agent secret", type="password", label_visibility="collapsed")
        
        if st.button("Se connecter au réseau"):
            user = next((emp for emp in st.session_state.employes if emp["Code"] == code_saisi), None)
            if user:
                st.session_state.authentifie = True
                st.session_state.utilisateur_actif = user["Nom"]
                st.session_state.registre_acces.append({
                    "Utilisateur": user["Nom"], "Poste": user["Poste"], "Heure": datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
                })
                st.success(f"Identification réussie. Bienvenue {user['Nom']} !")
                st.rerun()
            else:
                st.error("Code d'accès invalide.")
    st.stop()

# --- BARRE LATÉRALE ET NAVIGATION ---
st.sidebar.image(LOGO_NEGAGRI_REAL, width=120)
st.sidebar.title("NEGAGRI")
st.sidebar.write(f"👤 Connecté : **{st.session_state.utilisateur_actif}**")

if st.sidebar.button("🚪 Déconnexion"):
    st.session_state.authentifie = False
    st.session_state.utilisateur_actif = None
    st.rerun()

choix_menu = st.sidebar.radio(
    "Menu Général",
    ["🏠 Tableau de bord", "🌾 Production & Stocks", "🐛 Éleveurs de Hannetons", "💰 Ventes & Clients", "👥 Ressources Humaines", "📣 Communication", "🛡️ Sécurité"]
)

df_stocks = pd.DataFrame(list(st.session_state.stocks.items()), columns=["Produit", "Quantité"])

