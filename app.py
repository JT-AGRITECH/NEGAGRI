import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, time
from zoneinfo import ZoneInfo
import os

# --- CONFIGURATION GLOBALE ---
st.set_page_config(page_title="NEGAGRI - Gestion Industrielle", page_icon="🌾", layout="wide")

TZ_YAOUNDE = ZoneInfo("Africa/Douala")
HEURE_OUVERTURE = time(6, 0)
HEURE_FERMETURE = time(21, 0)

# Logo local - version transparente générée automatiquement
LOGO_PATH = "assets/logo_negagri.png"
DB_PATH = "negagri.db"

# --- BASE DE DONNEES PERSISTANTE ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS stocks (produit TEXT PRIMARY KEY, quantite INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS employes (nom TEXT, poste TEXT, salaire INTEGER, code TEXT PRIMARY KEY)')
    c.execute('CREATE TABLE IF NOT EXISTS eleveurs (nom TEXT, secteur TEXT, bacs_actifs INTEGER, total_livre INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS ventes (date TEXT, client TEXT, produit TEXT, quantite INTEGER, total INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (date TEXT, auteur TEXT, texte TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS incidents (date TEXT, type TEXT, secteur TEXT, gravite TEXT)')

    c.execute('SELECT COUNT(*) FROM stocks')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO stocks VALUES (?,?)', [
            ("Manioc (Kg)", 1500), ("Maïs (Sacs)", 320), ("Noix de Coco", 4500), 
            ("Hannetons (Bacs)", 85), ("Escargots (Kilos)", 120)
        ])
        c.executemany('INSERT INTO employes VALUES (?,?,?,?)', [
            ("Bella", "Directrice Générale", 500000, "0000"),
            ("Jean Mandeng", "Chef Élevage Hannetons", 85000, "1234"),
            ("Marie Ngo", "Responsable Transfo Manioc", 90000, "5678")
        ])
        c.executemany('INSERT INTO eleveurs VALUES (?,?,?,?)', [
            ("Amadou Diallo", "Obala", 12, 45), ("Chantal Biya II", "Mbalmayo", 8, 20)
        ])
        c.execute('INSERT INTO ventes VALUES (?,?,?,?,?)', ("2026-09-26", "Coopérative Centre", "Manioc (Kg)", 500, 150000))
        c.execute('INSERT INTO messages VALUES (?,?,?)', ("2026-09-25", "Bella", "Lancement officiel de la plateforme industrielle."))
        c.execute('INSERT INTO incidents VALUES (?,?,?,?)', ("2026-09-27", "Coupure Électricité", "Hangar Hannetons", "Moyenne"))
    conn.commit()
    conn.close()

def get_df(table):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

init_db()

# --- STYLES CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display:none;}
    .welcome-title { color: #005c2d; text-align: center; font-weight: bold; font-size: 3rem; margin-top:10px; }
    .welcome-subtitle { text-align: center; color: #7cb342; font-size: 1.3rem; margin-bottom: 35px; }
    .stButton>button { width: 100%; background-color: #005c2d; color: white; border-radius: 8px; font-weight: bold; border: none; padding: 10px; }
    .stButton>button:hover { background-color: #198754; color: white; }
    .card { padding: 25px; background-color: white; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.06); margin-bottom: 20px; border-left: 5px solid #005c2d; }
    h1, h2, h3 { color: #005c2d; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION ---
if 'authentifie' not in st.session_state:
    st.session_state.authentifie = False
    st.session_state.utilisateur_actif = None
    st.session_state.poste_actif = None
if 'registre_acces' not in st.session_state:
    st.session_state.registre_acces = []

# --- VERIFICATION HORAIRE YAOUNDE ---
heure_actuelle = datetime.now(TZ_YAOUNDE).time()
if not (HEURE_OUVERTURE <= heure_actuelle <= HEURE_FERMETURE):
    st.error(f"🔒 **NEGAGRI est fermée.** Ouverture de {HEURE_OUVERTURE.strftime('%H:%M')} à {HEURE_FERMETURE.strftime('%H:%M')} (Heure de Yaoundé). Il est {heure_actuelle.strftime('%H:%M')}.")
    st.stop()

# --- LOGIN ---
if not st.session_state.authentifie:
    st.markdown('<div class="welcome-title">NEGAGRI</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Nouvelle Génération Africaine de l\'Agriculture</div>', unsafe_allow_html=True)
    _, col_c, _ = st.columns([1, 1.4, 1])
    with col_c:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        else:
            st.markdown("### 🌾 NEGAGRI")
        st.subheader("🔑 Authentification")
        code_saisi = st.text_input("Code agent secret", type="password", placeholder="Ex: 0000")
        if st.button("Se connecter au réseau"):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT nom, poste FROM employes WHERE code =?', (code_saisi,))
            user = c.fetchone()
            conn.close()
            if user:
                st.session_state.authentifie = True
                st.session_state.utilisateur_actif = user[0]
                st.session_state.poste_actif = user[1]
                st.session_state.registre_acces.append({
                    "Utilisateur": user[0], "Poste": user[1], 
                    "Heure": datetime.now(TZ_YAOUNDE).strftime("%d/%m/%Y à %H:%M:%S")
                })
                st.success(f"Bienvenue {user[0]}!")
                st.rerun()
            else:
                st.error("Code d'accès invalide.")
    st.stop()

# --- SIDEBAR ---
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=160)
st.sidebar.title("NEGAGRI")
st.sidebar.write(f"👤 **{st.session_state.utilisateur_actif}**")
st.sidebar.caption(f"{st.session_state.poste_actif}")

if st.sidebar.button("🚪 Déconnexion"):
    st.session_state.authentifie = False
    st.session_state.utilisateur_actif = None
    st.rerun()

choix_menu = st.sidebar.radio("Menu Général", ["🏠 Tableau de bord", "🌾 Production & Stocks", "🐛 Éleveurs de Hannetons", "💰 Ventes & Clients", "👥 Ressources Humaines", "📣 Communication", "🛡 Sécurité"])

# Données
stocks_df = get_df("stocks")
stocks_dict = dict(zip(stocks_df['produit'], stocks_df['quantite'])) if not stocks_df.empty else {}

# --- ONGLETS ---
if choix_menu == "🏠 Tableau de bord":
    st.title("🏭 Rapport Industriel NEGAGRI")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Manioc Restant", f"{stocks_dict.get('Manioc (Kg)',0)} Kg")
    col2.metric("Hannetons Disponibles", f"{stocks_dict.get('Hannetons (Bacs)',0)} Bacs")
    col3.metric("Escargots", f"{stocks_dict.get('Escargots (Kilos)',0)} Kilos")
    df_eleveurs = get_df("eleveurs")
    col4.metric("Réseau Partenaires", f"{len(df_eleveurs)} Éleveurs")
    
    st.subheader("📊 Graphique des volumes de hangars")
    if not stocks_df.empty:
        st.bar_chart(stocks_df.set_index("Produit") if "Produit" in stocks_df.columns else stocks_df.set_index("produit"))
    
    st.subheader("📜 Dernières ventes")
    st.dataframe(get_df("ventes").tail(5), use_container_width=True, hide_index=True)

elif choix_menu == "🌾 Production & Stocks":
    st.title("🌾 Gestion de la Production Interne & Stocks")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📥 Enregistrer une nouvelle récolte")
        produit_select = st.selectbox("Choisir le produit", list(stocks_dict.keys()))
        quantite_ajout = st.number_input("Quantité produite", min_value=1, value=10)
        if st.button("Valider la production"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute('UPDATE stocks SET quantite = quantite + ? WHERE produit = ?', (quantite_ajout, produit_select))
            conn.commit()
            conn.close()
            st.success(f"Stock de {produit_select} mis à jour !")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.subheader("📦 État actuel des hangars")
        st.dataframe(get_df("stocks"), use_container_width=True, hide_index=True)

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
                conn = sqlite3.connect(DB_PATH)
                conn.execute('INSERT INTO eleveurs VALUES (?,?,?,?)', (n_coop, secteur, bacs, 0))
                conn.commit()
                conn.close()
                st.success("Nouvel éleveur enregistré !")
                st.rerun()
            else:
                st.error("Remplis tous les champs.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.subheader("📋 Liste des producteurs sous contrat")
        st.dataframe(get_df("eleveurs"), use_container_width=True, hide_index=True)

elif choix_menu == "💰 Ventes & Clients":
    st.title("💰 Facturation & Suivi du Chiffre d'Affaires")
    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🛒 Enregistrer un bon de commande")
        client = st.text_input("Nom de l'acheteur")
        prod = st.selectbox("Produit vendu", list(stocks_dict.keys()))
        qte = st.number_input("Quantité achetée", min_value=1, value=10)
        pu = st.number_input("Prix unitaire (FCFA)", min_value=50, value=500, step=50)
        if st.button("Émettre la facture"):
            if not client:
                st.error("Nom client requis.")
            elif stocks_dict.get(prod,0) < qte:
                st.error("Stock insuffisant.")
            else:
                total_fcfa = qte * pu
                conn = sqlite3.connect(DB_PATH)
                conn.execute('UPDATE stocks SET quantite = quantite - ? WHERE produit = ?', (qte, prod))
                conn.execute('INSERT INTO ventes VALUES (?,?,?,?,?)', (datetime.now(TZ_YAOUNDE).strftime("%Y-%m-%d"), client, prod, qte, total_fcfa))
                conn.commit()
                conn.close()
                st.success(f"Facture validée : {total_fcfa} FCFA")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        df_v = get_df("ventes")
        st.subheader("📜 Grand livre des ventes")
        st.dataframe(df_v, use_container_width=True, hide_index=True)
        if not df_v.empty:
            st.metric("Chiffre d'Affaires Total", f"{df_v['total'].sum():,} FCFA")

elif choix_menu == "👥 Ressources Humaines":
    st.title("👥 Ressources Humaines")
    st.dataframe(get_df("employes"), use_container_width=True, hide_index=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ Ajouter un employé")
    nom = st.text_input("Nom complet")
    poste = st.text_input("Poste")
    salaire = st.number_input("Salaire (FCFA)", min_value=0, value=80000, step=5000)
    code = st.text_input("Code d'accès (4 chiffres)")
    if st.button("Enregistrer l'employé"):
        if nom and poste and code:
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute('INSERT INTO employes VALUES (?,?,?,?)', (nom, poste, salaire, code))
                conn.commit()
                conn.close()
                st.success("Employé ajouté !")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Ce code existe déjà.")
        else:
            st.error("Tous les champs sont requis.")
    st.markdown('</div>', unsafe_allow_html=True)

elif choix_menu == "📣 Communication":
    st.title("📣 Fil d'Actualité Interne")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    msg = st.text_area("Nouveau message pour l'équipe")
    if st.button("Publier"):
        if msg:
            conn = sqlite3.connect(DB_PATH)
            conn.execute('INSERT INTO messages VALUES (?,?,?)', (datetime.now(TZ_YAOUNDE).strftime("%Y-%m-%d %H:%M"), st.session_state.utilisateur_actif, msg))
            conn.commit()
            conn.close()
            st.success("Message publié!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    df_msg = get_df("messages").sort_values("date", ascending=False) if not get_df("messages").empty else pd.DataFrame()
    for _, m in df_msg.iterrows():
        st.info(f"**{m['auteur']}** le {m['date']} - {m['texte']}")

elif choix_menu == "🛡 Sécurité":
    st.title("🛡 Sécurité & Incidents")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚨 Déclarer un incident")
        type_inc = st.selectbox("Type", ["Coupure Électricité", "Fuite Eau", "Vol", "Maladie Bacs", "Autre"])
        secteur_inc = st.text_input("Secteur concerné")
        gravite = st.select_slider("Gravité", options=["Faible", "Moyenne", "Critique"])
        if st.button("Signaler"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute('INSERT INTO incidents VALUES (?,?,?,?)', (datetime.now(TZ_YAOUNDE).strftime("%Y-%m-%d %H:%M"), type_inc, secteur_inc, gravite))
            conn.commit()
            conn.close()
            st.success("Incident enregistré!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.subheader("📋 Registre d'accès (session)")
        st.dataframe(pd.DataFrame(st.session_state.registre_acces), use_container_width=True, hide_index=True)

    st.subheader("📋 Historique des incidents")
    st.dataframe(get_df("incidents"), use_container_width=True, hide_index=True)
