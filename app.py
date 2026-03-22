import streamlit as st
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="TEP - Tire Exchange Program", layout="wide", page_icon="🛞")

# Titolo Principale
st.title("🛞 TEP: Tire Exchange Program")
st.markdown("---")
st.info("Benvenuto nel portale TEP. Seleziona l'agente e il cliente per calcolare lo stock restituibile.")

# Funzione per caricare i dati (Manteniamo i dati di test per ora)
@st.cache_data
def load_data():
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
st.sidebar.header("Filtri di Ricerca")
agente = st.sidebar.selectbox("👤 Seleziona Agente", df['Agente'].unique())
df_filtrato_agente = df[df['Agente'] == agente]

cliente = st.sidebar.selectbox("🏢 Seleziona Cliente", df_filtrato_agente['Cliente'].unique())
df_finale = df_filtrato_agente[df_filtrato_agente['Cliente'] == cliente]

# --- VISUALIZZAZIONE RISULTATI ---
st.subheader(f"Analisi Stock Restituibile: {cliente}")

# Qui mostriamo i risultati
st.dataframe(df_finale, use_container_width=True)

# Spazio per il pulsante
st.markdown("---")
csv = df_finale.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Scarica Modulo Reso TEP (Excel/CSV)",
    data=csv,
    file_name=f"TEP_Reso_{cliente}.csv",
    mime='text/csv',
)
