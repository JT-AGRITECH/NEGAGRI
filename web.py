import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_library

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="NEGAGRI - Gestion Industrielle", page_icon="🏢", layout="wide")

# Définition des horaires d'ouverture (06:00 à 21:00)
HEURE_OUVERTURE = time(6, 0)
HEURE_FERMETURE = time(21, 0)

# --- LOGO OFFICIEL NEGAGRI INTÉGRÉ (Encodé en Base64 pour une autonomie totale en ligne) ---
LOGO_NEGAGRI_AUTONOME = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj4KICAgIDxjaXJjbGUgY3g9IjI1NiIgY3k9IjI1NiIgcj0iMjQwIiBmaWxsPSIjMUI1RTIwIiBzdHJva2U9IiM4QkMzNEEiIHN0cm9rZS13aWR0aD0iMTIiLz4KICAgIDx0ZXh0IHg9IjI1NiIgeT0iMjkwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTIwIiBmb250LXdlaWdodD0iYm9sZCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPk4uQS48L3RleHQ+CiAgICA8cGF0aCBkPSJNMTIwIDM4MCBRMjU2IDMyMCAzOTIgMzgwIiBzdHJva2U9IiM4QkMzNEEiIHN0cm9rZS13aWR0aD0iMTYiIGZpbGw9Im5vbmUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4="

# --- STYLES CSS, ANIMATIONS ET SUPPRESSIONS ---
st.markdown("""
    <style>
    /* Supprime définitivement l'en-tête Streamlit et les menus d'origine */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Animation d'apparition fluide (Fade-In) */
    @keyframes fadeIn { 
        from { opacity: 0; transform: translateY(15px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    /* Style du Titre et du Logo Animé */
    .welcome-title { animation: fadeIn 1.2s ease-in-out; color: #1B5E20; text-align: center; font-weight: bold; font-size: 3rem; margin-top: 10px; }
    .welcome-subtitle { animation: fadeIn 1.8s ease-in-out; text-align: center; color: #558B2F; font-size: 1.4rem; margin-bottom: 40px; }
    
    /* Design général de l'usine numérique */
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #2E7D32; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #1B5E20; color: white; }
    .card { padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    h1, h2, h3 { color: #1B5E20; }
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
    st.info(f"⏰ Horaires d'accès autorisés : de **{HEURE_OUVERTURE.strftime('%H:%M')}** à **{HEURE_FERMETURE.strftime('%H:%M')}**.")
    st.stop()

# --- INTERFACE DE BIENVENUE ANIMÉE ET SÉCURISÉE ---
if not st.session_state.authentifie:
    st.markdown('<div class="welcome-title">NEGAGRI</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Système Industriel de Gestion Agricole & d\'Élevage</div>', unsafe_allow_html=True)
    
    col_vide1, col_centre, col_vide2 = st.columns([1, 2, 1])
    
    with col_centre:
        # Affichage direct et centré du logo autonome à partir du Base64
        st.image(LOGO_NEGAGRI_AUTONOME, width=160)

        st.subheader("🔑 Connexion Sécurisée")
        code_saisi = st.text_input("Entrez votre code d'accès personnel", type="password", label_visibility="collapsed")
        
        if st.button("Se connecter au Complexe Industriel"):
            utilisateur_trouve = next((emp for emp in st.session_state.employes if emp["Code"] == code_saisi), None)
            
            if utilisateur_trouve:
                st.session_state.authentifie = True
                st.session_state.utilisateur_actif = utilisateur_trouve["Nom"]
                
                st.session_state.registre_acces.append({
                    "Utilisateur": utilisateur_trouve["Nom"],
                    "Poste": utilisateur_trouve["Poste"],
                    "Heure de Connexion": datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
                })
                
                with st.spinner("Vérification des droits d'accès..."):
                    time_library.sleep(0.8)
                st.success(f"Accès accordé. Bienvenue {utilisateur_trouve['Nom']} !")
                st.rerun()
            else:
                st.error("Code d'accès incorrect. Veuillez réessayer.")
    st.stop()

# --- BARRE LATÉRALE : MENU DE NAVIGATION ---
st.sidebar.image(LOGO_NEGAGRI_AUTONOME, width=90)
st.sidebar.title("NEGAGRI")
st.sidebar.write(f"👤 Session : **{st.session_state.utilisateur_actif}**")

if st.sidebar.button("🚪 Se déconnecter"):
    st.session_state.authentifie = False
    st.session_state.utilisateur_actif = None
    st.rerun()

choix_menu = st.sidebar.radio(
    "Menu de navigation",
    ["🏠 Tableau de bord", "🌾 Production & Stocks", "🐛 Éleveurs de Hannetons", "💰 Ventes & Clients", "👥 Ressources Humaines", "📣 Communication", "🛡️ Sécurité"]
)

df_stocks = pd.DataFrame(list(st.session_state.stocks.items()), columns=["Produit", "Quantité"])

# ==========================================
# GESTION DES ONGLETS
# ==========================================
if choix_menu == "🏠 Tableau de bord":
    st.title("🏭 Tableau de Bord NEGAGRI")
    st.write(f"Rapport d'activité généré par **{st.session_state.utilisateur_actif}**.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="Manioc en Stock", value=f"{st.session_state.stocks['Manioc (Kg)']} Kg")
    with col2: st.metric(label="Total Hannetons en Stock", value=f"{st.session_state.stocks['Hannetons (Bacs)']} Bacs")
    with col3: st.metric(label="Éleveurs Partenaires", value=len(st.session_state.eleveurs))
    with col4: st.metric(label="Statut Horaire", value="Ouvert", delta=f"Ferme à {HEURE_FERMETURE.strftime('%H:%M')}")

    st.subheader("📊 Graphique de Production Global")
    st.bar_chart(df_stocks.set_index("Produit"))

elif choix_menu == "🌾 Production & Stocks":
    st.title("🌾 Gestion de la Production Interne & Stocks")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📥 Enregistrer une récolte propre")
        produit_select = st.selectbox("Choisir le produit", list(st.session_state.stocks.keys()))
        quantite_ajout = st.number_input("Quantité produite", min_value=1, value=10)
        if st.button("Valider la production"):
            st.session_state.stocks[produit_select] += quantite_ajout
            st.success(f"Stock de {produit_select} mis à jour !")
            st.rerun()
            
    with col2:
        st.subheader("📦 État actuel des hangars")
        st.dataframe(df_stocks, use_container_width=True)

else:
    st.title(f"{choix_menu}")
    st.info("Cette section est prête à recevoir ses fonctionnalités spécifiques.")
