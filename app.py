import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. CSS SEMPLIFICATO E PULITO (Niente riquadri, focus su leggibilità)
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }
    .stAlert { background-color: #FBBD00 !important; border: none; }
    .stAlert p { color: #0B1D45 !important; font-weight: bold; }

    /* SIDEBAR GIALLA */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { 
        color: #0B1D45 !important; 
        font-weight: bold !important; 
    }

    /* STILE SELECT SLIDER (Il nuovo selettore) */
    div[data-role="stSelectSlider"] { margin-bottom: 20px; }
    
    /* DROPDOWN MENU */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        background-color: #0B1D45 !important;
        border-radius: 4px !important;
    }
    div[data-baseweb="select"] div { color: #FBBD00 !important; }

    /* TABELLA E INTESTAZIONI */
    .stDataFrame { background-color: #FFFFFF !important; border-radius: 8px; }
    
    /* Centratura e grassetto per intestazioni tabella */
    [data-testid="stTable"] th, [data-testid="stDataFrame"] th {
        text-align: center !important;
        font-weight: bold !important;
        color: #0B1D45 !important;
        text-transform: uppercase;
    }

    /* BOTTONE DOWNLOAD */
    .stDownloadButton button { 
        background-color: #FBBD00 !important; 
        color: #0B1D45 !important; 
        border: 2px solid #0B1D45 !important; 
        font-weight: bold; width: 100%;
    }
    .stDownloadButton button:hover { background-color: #FFFFFF !important; border-color: #0B1D45 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATI DI TEST
@st.cache_data
def load_data():
    data = {
        'Sales Representative': ['Mario Rossi', 'Mario Rossi', 'Luigi Bianchi', 'Luigi Bianchi'],
        'Codice Cliente': ['A105', 'B200', 'C001', 'A050'],
        'Nome Cliente': ['Zeta Tyres', 'Alpha Gomme', 'Beta Ruote', 'Delta Service'],
        'Size & Type': ['205/55 R16 Summer', '225/45 R17 Winter', '195/65 R15 AllSeason', '245/40 R18 Sport'],
        'Quantità Iniziale': [10, 20, 15, 30],
        'Quantità restituibile': [7, 14, 0, 21]
    }
    return pd.DataFrame(data)

df = load_data()

# --- INTERFACCIA SIDEBAR ---

with st.sidebar:
    st.subheader("👤 Sales Representative")
    sales_reps = sorted(df['Sales Representative'].unique())
    sales_rep = st.selectbox("Seleziona il tuo nome", sales_reps)

    st.markdown("---")
    st.subheader("🔍 Ricerca Cliente")
    
    df_rep = df[df['Sales Representative'] == sales_rep]
    nomi_lista = sorted(df_rep['Nome Cliente'].unique())
    codici_lista = sorted(df_rep['Codice Cliente'].unique())

    # NUOVO SELECT SLIDER: A sinistra Codice, a destra Ragione Sociale
    modalita = st.select_slider(
        "Scegli modalità di ricerca:",
        options=["Codice Cliente", "Ragione Sociale"],
        value="Ragione Sociale"
    )

    if modalita == "Ragione Sociale":
        cliente_nome = st.selectbox("Seleziona Nome", nomi_lista)
        cliente_codice = df_rep[df_rep['Nome Cliente'] == cliente_nome]['Codice Cliente'].iloc[0]
    else:
        cliente_codice = st.selectbox("Seleziona Codice", codici_lista)
        cliente_nome = df_rep[df_rep['Codice Cliente'] == cliente_codice]['Nome Cliente'].iloc[0]

# --- VISUALIZZAZIONE PRINCIPALE ---
st.title("🛞 TEP: Tire Exchange Program")
st.info("Portale per la gestione dei resi pneumatici stagionali.")

st.subheader(f"Riepilogo pneumatici restituibili: {cliente_nome}")
st.write(f"**Codice Cliente:** {cliente_codice} | **Sales Rep:** {sales_rep}")

# PREPARAZIONE E STILIZZAZIONE TABELLA
df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice].copy()

if not df_display.empty:
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']]
    
    # Applicazione stile: centrato per le quantità, grassetto per la restituibile
    styled_df = df_view.style.set_properties(**{
        'text-align': 'center'
    }, subset=['Quantità Iniziale', 'Quantità restituibile']).set_properties(**{
        'font-weight': 'bold'
    }, subset=['Quantità restituibile'])
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 SCARICA MODULO RESO PER {cliente_nome}", 
        data=csv, 
        file_name=f"TEP_{cliente_codice}.csv", 
        mime='text/csv'
    )
