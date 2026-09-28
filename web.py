import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_library

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="NEGAGRI - Gestion Industrielle", page_icon="🌾", layout="wide")

# Définition des horaires d'ouverture (06:00 à 21:00)
HEURE_OUVERTURE = time(6, 0)
HEURE_FERMETURE = time(21, 0)

# --- LIEN DIRECT VERS LE LOGO OFFICIEL SUR GITHUB (Évite les bugs de copier-coller) ---
LOGO_NEGAGRI_URL = "https://githubusercontent.com"

# --- STYLES CSS PERSONNALISÉS (Thème Charte Graphique NEGAGRI) ---
st.markdown("""
    <style>
    /* Supprime définitivement l'en-tête, le footer et le bouton Deploy de Streamlit */
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display:none;}
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .welcome-title { animation: fadeIn 1.2s ease-in-out; color: #005c2d; text-align: center; font-weight: bold; font-size: 3rem; margin-top: 10px; }
    .welcome-subtitle { animation: fadeIn 1.6s ease-in-out; text-align: center; color: #7cb342; font-size: 1.3rem; margin-bottom: 35px; }
    .stButton>button { width: 100%; background-color: #005c2d; color: white; border-radius: 8px; font-weight: bold; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #198754; color: white; }
    .card { padding: 25px; background-color: white; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); margin-bottom: 20px; border-left: 5px solid #005c2d; }
    h1, h2, h3 { color: #005c2d; }
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
        # Affichage sécurisé via l'URL GitHub
        st.image(LOGO_NEGAGRI_URL, use_container_width=True)
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
st.sidebar.image(LOGO_NEGAGRI_URL, width=140)
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
# PROGRAMMATION DES ONGLETS COMPLETS
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
                st.session_state.eleveurs.append({"Nom/Coopérative": n_coop, "Secteur": secteur, "Bacs Actifs": bacs, "Total Livré (Bacs)": 0})
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
        pu = st.number_input("Prix unitaire (FCFA)", min_value=50, value=500, step=50)
        
        if st.button("Émettre la facture"):
            if client and st.session_state.stocks[prod] >= qte:
                total_fcfa = qte * pu
                st.session_state.stocks[prod] -= qte
                st.session_state.ventes.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Client": client, "Produit": prod, "Quantité": qte, "Total (FCFA)": total_fcfa})
                st.success(f"Facture validée : {total_fcfa} FCFA. Stock déduit !")
                st.rerun()
            elif st.session_state.stocks[prod] < qte:
                st.error("Stock insuffisant pour couvrir cette commande.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.subheader("📜 Grand livre des ventes enregistrées")
        df_v = pd.DataFrame(st.session_state.ventes)
