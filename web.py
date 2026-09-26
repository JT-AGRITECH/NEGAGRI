import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_library

# --- CONFIGURATION GLOBALE ---
# L'icône de la page (page_icon) utilise un émoji neutre puisque le tracteur est supprimé
st.set_page_config(page_title="NEGAGRI - Gestion Industrielle", page_icon="🏢", layout="wide")

# Définition des horaires d'ouverture (06:00 à 21:00)
HEURE_OUVERTURE = time(6, 0)
HEURE_FERMETURE = time(21, 0)

# --- LOGO OFFICIEL NEGAGRI EN CODE PUR (Évite le carré blanc) ---
# Ce code représente textuellement une image de logo agricole circulaire et moderne
LOGO_BASE64 = "data:image/svg+xml;utf8,<svg xmlns='http://w3.org' viewBox='0 0 100 100'><circle cx='50' cy='50' r='45' fill='%231B5E20'/><path d='M35 65 V 35 L 50 50 L 65 35 V 65' stroke='white' stroke-width='8' fill='none' stroke-linecap='round' stroke-linejoin='round'/><leaf xmlns='http://w3.org' d='M50 20 Q65 20 65 35 Q50 35 50 20' fill='%238BC34A'/></svg>"

# --- STYLES CSS, ANIMATIONS ET SUPPRESSIONS ---
st.markdown("""
    <style>
    /* 1. Supprime définitivement le logo rouge Streamlit, le tracteur et les menus d'origine */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 2. Animation d'apparition fluide (Fade-In) */
    @keyframes fadeIn { 
        from { opacity: 0; transform: translateY(15px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    /* Style du Titre et du Logo Animé */
    .welcome-title { animation: fadeIn 1.2s ease-in-out; color: #1B5E20; text-align: center; font-weight: bold; font-size: 3rem; margin-top: 10px; }
    .welcome-subtitle { animation: fadeIn 1.8s ease-in-out; text-align: center; color: #558B2F; font-size: 1.4rem; margin-bottom: 40px; }
    
    .avatar-container { animation: fadeIn 1.5s ease-in-out; display: flex; justify-content: center; margin-bottom: 25px; }
    .animated-logo { width: 180px; height: 180px; border-radius: 50%; box-shadow: 0 8px 20px rgba(0,0,0,0.15); background-color: white; padding: 10px; }
    
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
    
    # Centre complet du logo et du formulaire de connexion
    col_vide1, col_centre, col_vide2 = st.columns([1, 2, 1])
    
    with col_centre:
        # Affichage du logo NEGAGRI animé de manière centrée et propre
        st.markdown(f'<div class="avatar-container"><img src="{LOGO_BASE64}" class="animated-logo" alt="Logo NEGAGRI"></div>', unsafe_allow_html=True)
        
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
                
                with st.spinner("Vérification biométrique virtuelle..."):
                    time_library.sleep(0.8)
                st.success(f"Accès accordé. Bienvenue {utilisateur_trouve['Nom']} !")
                st.rerun()
            else:
                st.error("Code d'accès incorrect. Veuillez réessayer.")
    st.stop()

# --- BARRE LATÉRALE : MENU DE NAVIGATION ---
st.sidebar.markdown(f'<div class="avatar-container"><img src="{LOGO_BASE64}" style="width:90px; height:90px; border-radius:50%;" alt="Logo NEGAGRI"></div>', unsafe_allow_html=True)
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
            st.success(f"Stock de {produit_select} mis à jour par {st.session_state.utilisateur_actif} !")
            st.rerun()
    with col2:
        st.subheader("📦 État des Silos et Bacs")
        st.table(df_stocks)

elif choix_menu == "🐛 Éleveurs de Hannetons":
    st.title("🐛 Gestion du Réseau d'Éleveurs Indépendants")
    col_el1, col_el2 = st.columns(2)
    with col_el1:
        st.subheader("📋 Liste des Éleveurs Partenaires")
        st.dataframe(pd.DataFrame(st.session_state.eleveurs), use_container_width=True)
        with st.expander("➕ Enregistrer un nouvel éleveur"):
            nom_el = st.text_input("Nom de l'éleveur ou de la Coopérative")
            secteur_el = st.text_input("Secteur Géographique")
            bacs_el = st.number_input("Nombre de bacs actifs", min_value=0, value=5)
            if st.button("Enregistrer le Partenaire"):
                if nom_el:
                    st.session_state.eleveurs.append({"Nom/Coopérative": nom_el, "Secteur": secteur_el, "Bacs Actifs": bacs_el, "Total Livré (Bacs)": 0})
                    st.success(f"Éleveur {nom_el} enregistré !")
                    st.rerun()
    with col_el2:
        st.subheader("📥 Acheter la production d'un éleveur")
        if st.session_state.eleveurs:
            liste_el = [e["Nom/Coopérative"] for e in st.session_state.eleveurs]
            el_selectionne = st.selectbox("Choisir l'éleveur", liste_el)
