import streamlit as st
import pandas as pd

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# 2. CSS "HARDCORE" PER COSTRINGERE L'INTERFACCIA
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

    /* --- FIX CHECKBOX: BORDO BLU NETTO --- */
    /* Forza il bordo del quadratino quando è vuoto */
    div[data-testid="stCheckbox"] div[data-baseweb="checkbox"] {
        border: 2px solid #0B1D45 !important;
    }
    /* Forza il colore quando è selezionato */
    div[data-testid="stCheckbox"] div[aria-checked="true"] {
        background-color: #0B1D45 !important;
    }

    /* --- FIX TABELLA (st.table) --- */
    /* Forza ALLINEAMENTO CENTRALE su titoli e celle */
    table {
        width: 100%;
        background-color: white !important;
        color: #0B1D45 !important;
        border-radius: 10px;
    }
    th {
        text-align: center !important;
        font-weight: bold !important;
        background-color: #f0f2f6 !important;
    }
    td {
        text-align: center !important;
        vertical-align: middle !important;
    }
    /* Grassetto per l'ultima colonna (Quantità restituibile) */
    td:last-child {
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

# --- SIDEBAR ---
with st.sidebar:
    st.subheader("👤 Sales Representative")
    sales_reps = sorted(df['Sales Representative'].unique())
    sales_rep = st.selectbox("Scegli Sales Rep", sales_reps, label_visibility="collapsed")

    st.markdown("---")
    st.subheader("🔍 Ricerca Cliente")
    
    # La checkbox ora ha il bordo forzato via CSS
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

# --- MAIN ---
st.title("🛞 TEP: Tire Exchange Program")

st.subheader(f"Riepilogo pneumatici restituibili: {cliente_nome}")
st.write(f"**Codice:** {cliente_codice} | **Sales Rep:** {sales_rep}")

df_display = df_rep[df_rep['Codice Cliente'] == cliente_codice].copy()

if not df_display.empty:
    # Usiamo st.table invece di st.dataframe per avere il controllo totale del CSS
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']]
    st.table(df_view)
    
    st.markdown("---")
    csv = df_view.to_csv(index=False).encode('utf-8')
    st.download_button(label=f"📥 SCARICA MODULO RESO TEP", data=csv, file_name=f"TEP_{cliente_codice}.csv")
