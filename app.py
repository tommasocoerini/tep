import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. CSS "FORZATO" (SELETTORI AD ALTA SPECIFICITÀ)
st.markdown("""
    <style>
    .main { background-color: #0B1D45 !important; }
    h1 { color: #FBBD00 !important; font-weight: bold; }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #FBBD00 !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { 
        color: #0B1D45 !important; 
        font-weight: bold !important; 
    }

    /* --- FIX CHECKBOX: BORDO BLU VISIBILE --- */
    /* Questo punta direttamente al quadratino della checkbox */
    [data-testid="stCheckbox"] [data-checked="false"] {
        border: 2px solid #0B1D45 !important;
    }
    [data-testid="stCheckbox"] [data-checked="true"] {
        background-color: #0B1D45 !important;
        border: 2px solid #0B1D45 !important;
    }

    /* --- FIX TABELLA: ALLINEAMENTO CENTRALE --- */
    /* Forza l'allineamento di tutte le celle e delle intestazioni */
    [data-testid="stDataFrame"] div[data-testid="stTable"] th,
    [data-testid="stDataFrame"] div[data-testid="stTable"] td,
    div[role="gridcell"], 
    div[role="columnheader"] {
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Titoli in grassetto Blue */
    div[role="columnheader"] {
        font-weight: bold !important;
        color: #0B1D45 !important;
    }

    /* Grassetto per i dati della colonna Quantità Restituibile */
    [data-testid="stDataFrame"] div[role="row"] div[role="gridcell"]:nth-child(3) {
        font-weight: bold !important;
    }

    /* DROPDOWN MENU */
    div[data-baseweb="select"] { 
        border: 2px solid #0B1D45 !important; 
        background-color: #0B1D45 !important;
    }
    div[data-baseweb="select"] div { color: #FBBD00 !important; }

    /* BOTTONE DOWNLOAD */
    .stDownloadButton button { 
        background-color: #FBBD00 !important; 
        color: #0B1D45 !important; 
        border: 2px solid #0B1D45 !important; 
        font-weight: bold; width: 100%;
    }
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
    sales_rep = st.selectbox("Scegli Sales Rep", sales_reps, label_visibility="collapsed")

    st.markdown("---")
    st.subheader("🔍 Ricerca Cliente")
    
    # Checkbox
    usa_codice = st.checkbox("Cerca per Codice Cliente")
    
    df_rep = df[df['Sales Representative'] == sales_rep]
    
    if usa_codice:
        codici_lista = sorted(df_rep['Codice Cliente'].unique())
        cliente_codice = st.selectbox("Seleziona Codice Cliente", codici_lista)
        cliente_nome = df_rep[df_rep['Codice Cliente'] == cliente_codice]['Nome Cliente'].iloc[0]
    else:
        nomi_lista = sorted(df_rep['Nome Cliente'].unique())
        cliente_nome = st.selectbox("Seleziona Ragione Sociale", nomi_lista)
        cliente_codice = df_rep[df_rep['Nome Cliente'] == cliente_nome]['Codice Cliente'].iloc[0]

# --- VISUALIZZAZIONE PRINCIPALE ---
st.title("🛞 TEP: Tire Exchange Program")

st.subheader(f"Riepilogo pneumatici restituibili: {cliente_nome}")
st.write(f"**Codice:** {cliente_codice} | **Sales Rep:** {sales_rep}")

df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice].copy()

if not df_display.empty:
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']]
    
    # Utilizziamo st.table invece di st.dataframe se il problema persiste.
    # st.table è una tabella statica molto più facile da stilizzare con il CSS.
    st.table(df_view)
    
    st.markdown("---")
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 SCARICA MODULO RESO PER {cliente_nome}", 
        data=csv, 
        file_name=f"TEP_{cliente_codice}.csv", 
        mime='text/csv'
    )
