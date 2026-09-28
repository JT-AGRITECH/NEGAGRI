import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_library

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="NEGAGRI - Gestion Industrielle", page_icon="🌾", layout="wide")

# Définition des horaires d'ouverture (06:00 à 21:00)
HEURE_OUVERTURE = time(6, 0)
HEURE_FERMETURE = time(21, 0)

# --- VRAI LOGO NEGAGRI VECTORIEL OFFICIEL (Intégration native garantie 100% visible) ---
LOGO_NEGAGRI_SVG = """
<svg xmlns="http://w3.org" viewBox="0 0 300 300" style="width:100%; max-width:200px; display:block; margin:auto;">
    <!-- Symbole N stylisé en vert agropastoral profond -->
    <path d="M 60 220 L 60 80 L 110 80 L 190 190 L 190 80 L 230 80 L 230 220 L 180 220 L 100 110 L 100 220 Z" fill="#005c2d"/>
    <!-- Sillons agricoles dorés / orange à la base du logo -->
    <path d="M 60 230 Q 145 190 230 230" stroke="#d48c00" stroke-width="8" fill="none" stroke-linecap="round"/>
    <path d="M 80 242 Q 145 210 210 242" stroke="#d48c00" stroke-width="6" fill="none" stroke-linecap="round"/>
    <!-- Feuille de croissance sur le N -->
    <path d="M 100 110 Q 120 90 135 110 Q 115 125 100 110" fill="#7cb342"/>
</svg>
"""

# --- STYLES CSS PERSONNALISÉS (Thème Vert Agricole & Alignements) ---
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
    
    /* Centreur universel pour le logo de la page d'accueil */
    .logo-center-container { display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DONNÉES TEMPORAIRES EN MÉMOIRE ---
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
        # Injection du logo vectoriel pur au centre de la page
        st.markdown(f'<div class="logo-center-container">{LOGO_NEGAGRI_SVG}</div>', unsafe_allow_html=True)
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
st.sidebar.markdown(f'<div style="text-align:center; margin-bottom:15px;">{LOGO_NEGAGRI_SVG}</div>', unsafe_allow_html=True)
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

# =========================================================================================
# GESTION DES ONGLETS
# =========================================================================================

# 1. TABLEAU DE BORD
if choix_menu == "🏠 Tableau de bord":
    st.title("🏭 Rapport Industriel NEGAGRI")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Manioc Restant", f"{st.session_state.stocks['Manioc (Kg)']} Kg")
    with col2: st.metric("Hannetons Disponibles", f"{st.session_state.stocks['Hannetons (Bacs)']} Bacs")
    with col3: st.metric("Escargots", f"{st.session_state.stocks['Escargots (Kilos)']} Kilos")
    with col4: st.metric("Réseau Partenaires", f"{len(st.session_state.eleveurs)} Éleveurs")
    
    st.subheader("📊 Graphique des volumes de hangars")
    st.bar_chart(df_stocks.set_index("Produit"))

# 2. PRODUCTION & STOCKS
elif choix_menu == "🌾 Production & Stocks":
    st.title("🌾 Gestion de la Production Interne & Stocks")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📥 Enregistrer une nouvelle récolte")
        produit_select = st.selectbox("Choisir le produit", list(st.session_state.stocks.keys()))
        quantite_ajout = st.number_input("Quantité produite", min_value=1, value=10)
        if st.button("Valider la production"):
            st.session_state.stocks[produit_select] += quantite_ajout
            st.success(f"Stock de {produit_select} mis à jour !")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with col2:
        st.subheader("📦 État actuel des hangars")
        st.dataframe(df_stocks, use_container_width=True, hide_index=True)

# 3. ÉLEVEURS DE HANNETONS
elif choix_menu == "🐛 Éleveurs de Hannetons":
    st.title("🐛 Gestion des Réseaux d'Éleveurs Externes")
    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("➕ Enrôler un nouveau partenaire")
        n_coop = st.text_input("Nom de la structure / Éleveur")
        secteur = st.text_input("Localisation / Secteur (ex: Obala)")
        bacs = st.number_input("Nombre de bacs actifs distribués", min_value=1, value=5)
        if st.button("Inscrire dans la base"):
            if n_coop and secteur:
                st.session_state.eleveurs.append({"Nom/Coopérative": n_coop, "Secteur": secteur, "BActive": bacs, "Total Livré (Bacs)": 0})
                st.success("Nouvel éleveur enregistré !")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.subheader("📋 Liste des producteurs sous contrat")
        st.dataframe(pd.DataFrame(st.session_state.eleveurs), use_container_width=True, hide_index=True)

# 4. VENTES & CLIENTS
elif choix_menu == "💰 Ventes & Clients":
    st.title("💰 Facturation & Suivi du Chiffre d'Affaires")
    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🛒 Enregistrer un bon de commande")
        client = st.text_input("Nom de l'acheteur")
        prod = st.selectbox("Produit vendu", list(st.session_state.stocks.keys()))
        qte = st.number_input("Quantité achetée", min_value=1, value=10)
