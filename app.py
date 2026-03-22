import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. BLOCCO CSS PERSONALIZZATO (Il tuo "Centro Stile")
st.markdown("""
    <style>
    /* --- SFONDO E TESTI GENERALI --- */
    .main {
        background-color: #0B1D45; /* Colore sfondo pagina principale */
    }
    
    /* --- TITOLO PRINCIPALE (H1) --- */
    h1 {
        color: #FBBD00 !important; /* Blu scuro aziendale */
        font-weight: bold;
    }

    /* --- BOX BENVENUTO (st.info) --- */
    .stAlert {
        background-color: #FBBD00; /* Sfondo azzurrino */
        border: 1px solid #FBBD00;
    }
    .stAlert p {
        color: #0B1D45 !important; /* Colore testo dentro il box info */
        font-size: 1.1rem;
    }

    /* --- BARRA LATERALE (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: #FBBD00; /* Sfondo barra laterale (es. Blu) */
    }
    
    /* Titoli dei menu a tendina nella sidebar */
    [data-testid="stSidebar"] label {
        color: #0B1D45 !important; /* Bianco per i titoli dei menu */
        font-weight: bold;
    }

    /* Testo all'interno dei menu a tendina (le opzioni selezionate) */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #0B1D45 !important; /* Colore testo dentro il menu (Blu) */
        background-color: #FBBD00 !important; /* Sfondo bianco del menu */
    }

    /* --- TABELLE --- */
    /* Colore del testo nelle tabelle/dataframe */
    .stDataFrame, [data-testid="stTable"] {
        color: #FBBD00; 
        background-color: #FFFFFF;
    }

    /* --- BOTTONE DOWNLOAD --- */
    .stDownloadButton button {
        background-color: #FBBD00 !important; /* Rosso */
        color: white !important; /* Testo Bianco */
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stDownloadButton button:hover {
        background-color: #0B1D45 !important; /* Rosso più scuro al passaggio del mouse */
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGO (Opzionale)
# st.sidebar.image("link_al_tuo_logo.png")

# --- DA QUI IN POI IL TUO CODICE LOGICO ---
st.title("🛞 TEP: Tire Exchange Program")
st.info("Benvenuto nel portale TEP. Seleziona l'agente e il cliente per calcolare lo stock restituibile.")

# Funzione dati (Esempio)
@st.cache_data
def load_data():
    data = {
        'Agente': ['Mario Rossi', 'Luigi Bianchi'],
        'Cliente': ['Gommista A', 'Gommista B'],
        'SKU': ['PNEU-001', 'PNEU-002'],
        'Qta_Iniziale': [10, 20]
    }
    return pd.DataFrame(data)

df = load_data()

# Filtri
agente = st.sidebar.selectbox("👤 Seleziona Agente", df['Agente'].unique())
cliente = st.sidebar.selectbox("🏢 Seleziona Cliente", df[df['Agente']==agente]['Cliente'].unique())

# Visualizzazione
st.subheader(f"Analisi per: {cliente}")
st.dataframe(df[df['Cliente']==cliente], use_container_width=True)

st.download_button("📥 Scarica Modulo Reso TEP", "dati finti", "reso.csv")
