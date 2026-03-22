import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portale Resi Pneumatici", layout="wide")

st.title("📦 Gestione Resi Stock Iniziale")
st.info("Benvenuto. Seleziona il tuo nome e il cliente per verificare i prodotti restituibili.")

# Funzione per caricare i dati
@st.cache_data
def load_data():
    # Per ora creiamo dati finti per testare il sito
    data = {
        'Agente': ['Mario Rossi', 'Mario Rossi', 'Luigi Bianchi'],
        'Cliente': ['Gommista A', 'Gommista B', 'Gommista C'],
        'SKU': ['PNEU-001', 'PNEU-002', 'PNEU-003'],
        'Descrizione': ['Modello Summer 18"', 'Modello Winter 17"', 'All Season 16"'],
        'Qta_Iniziale': [10, 10, 10]
    }
    return pd.DataFrame(data)

df = load_data()

# --- FILTRI LATERALI ---
agente = st.sidebar.selectbox("1. Seleziona Agente", df['Agente'].unique())
df_filtrato_agente = df[df['Agente'] == agente]

cliente = st.sidebar.selectbox("2. Seleziona Cliente", df_filtrato_agente['Cliente'].unique())
df_finale = df_filtrato_agente[df_filtrato_agente['Cliente'] == cliente]

# --- VISUALIZZAZIONE ---
st.subheader(f"Analisi per: {cliente}")
st.write("Prodotti che non hanno subito riordini e sono idonei al reso:")
st.table(df_finale)

# Tasto Download
csv = df_finale.to_csv(index=False).encode('utf-8')
st.download_button("📥 Scarica Excel per Customer Service", csv, f"Reso_{cliente}.csv", "text/csv")
