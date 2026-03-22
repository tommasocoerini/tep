import streamlit as st
import pandas as pd
import io

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="TEP - Program 2026", layout="wide", page_icon="📊")

# LINK DIRETTI AI TUOI ASSET SU GITHUB
LOGO_MAIN    = "https://github.com/tommasocoerini/tep/blob/main/logo.png?raw=true"
LOGO_SIDEBAR = "https://github.com/tommasocoerini/tep/blob/main/logo2.png?raw=true"
# Link RAW per leggere il file Excel dei Sales Rep
SALES_REPS_URL = "https://github.com/tommasocoerini/tep/raw/1e81323d556f23bdbc49863f47faa8d26d4c0696/sales_reps.xlsx"

# ATTIVAZIONE LOGO SIDEBAR
st.logo(LOGO_SIDEBAR)

# 2. CSS COMPLETO
st.markdown(f"""
    <style>
    .main {{ background-color: #0B1D45 !important; }}

    /* SIDEBAR */
    [data-testid="stSidebar"] {{ background-color: #FBBD00 !important; }}

    /* HEADER SIDEBAR (LOGO) */
    [data-testid="stSidebarHeader"] {{
        background-color: #FBBD00 !important;
        background-image: url('{LOGO_SIDEBAR}') !important;
        background-repeat: no-repeat !important;
        background-size: contain !important;
        background-position: center !important;
        min-height: 120px !important;
        margin-top: -30px !important;
        padding: 0 !important;
    }}

    [data-testid="stLogo"] {{
        visibility: hidden !important;
        display: none !important;
    }}

    .sidebar-section-title {{
        color: #0B1D45 !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        margin-bottom: 8px !important;
        margin-top: 10px !important;
        display: block;
    }}

    div[data-baseweb="select"] {{
        border: 2px solid #0B1D45 !important;
        background-color: #0B1D45 !important;
    }}
    div[data-baseweb="select"] div {{ color: #FBBD00 !important; }}

    /* HEADER PRINCIPALE */
    .header-container {{
        display: flex; align-items: center;
        gap: 20px; padding-bottom: 20px;
    }}
    .logo-img {{ width: 80px; height: auto; }}
    .main-title {{
        color: #FBBD00 !important; font-weight: bold !important;
        font-size: 2.5rem !important; margin: 0 !important;
    }}
    .sub-title {{
        color: #FFFFFF !important; font-size: 1.1rem !important;
        margin: 0 !important; opacity: 0.8;
    }}

    /* TABELLA HTML */
    .tep-table {{
        width: 100%; border-collapse: separate; border-spacing: 0;
        border-radius: 12px; overflow: hidden;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 4px 24px rgba(0,0,0,0.4); margin-bottom: 25px;
    }}
    .tep-table thead tr {{ background-color: #FBBD00; }}
    .tep-table thead th {{
        color: #0B1D45 !important; font-weight: 800;
        text-transform: uppercase; padding: 12px 16px; text-align: center;
    }}
    .tep-table tbody tr:nth-child(odd)  {{ background-color: #112259; }}
    .tep-table tbody tr:nth-child(even) {{ background-color: #0D1D48; }}
    .tep-table tbody td {{ color: #E8EDF8 !important; padding: 11px 16px; text-align: center; }}
    .tep-table tbody td:first-child {{ text-align: left; padding-left: 20px; }}
    .tep-table tbody td:last-child {{ color: #FBBD00 !important; font-weight: 800; font-size: 1.1rem; }}

    .stDownloadButton button {{
        background-color: #FBBD00 !important;
        color: #0B1D45 !important;
        border: 2px solid #0B1D45 !important;
        font-weight: bold; width: 100%;
        padding: 15px; border-radius: 8px;
        text-transform: uppercase;
    }}
    </style>
""", unsafe_allow_html=True)

# 3. FUNZIONI DATI
@st.cache_data
def load_sales_reps():
    try:
        # Legge i Sales Rep dal tuo Excel su GitHub
        df_reps = pd.read_excel(SALES_REPS_URL)
        df_reps.columns = df_reps.columns.str.strip()
        return df_reps
    except Exception as e:
        st.error(f"Errore caricamento database agenti: {e}")
        return pd.DataFrame({'Sales Representative': ['Mario Rossi', 'Luigi Bianchi']})

@st.cache_data
def load_mock_data(reps_list):
    """Genera dati temporanei finché non avremo i file clienti reali"""
    data = []
    for i, rep in enumerate(reps_list):
        data.append({
            'Sales Representative': rep,
            'Codice Cliente': f'ABC{100+i}',
            'Nome Cliente': f'Cliente Demo {i+1}',
            'Size & Type': '205/55 R16 Summer',
            'Quantità Iniziale': 24,
            'Quantità restituibile': 12
        })
    return pd.DataFrame(data)

def to_excel(df, codice, ragione_sociale):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reso_TEP', startrow=3, header=False)
        workbook  = writer.book
        worksheet = writer.sheets['Reso_TEP']
        fmt_grigio_bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        fmt_header = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        fmt_normal = workbook.add_format({'border': 1})
        worksheet.write('A1', 'CODICE CLIENTE', fmt_grigio_bold)
        worksheet.write('B1', codice, fmt_normal)
        worksheet.write('A2', 'RAGIONE SOCIALE', fmt_grigio_bold)
        worksheet.write('B2', ragione_sociale, fmt_normal)
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(2, col_num, value, fmt_header)
        for i, col in enumerate(df.columns):
            max_val = df[col].astype(str).map(len).max() if not df.empty else 0
            max_len = max(max_val, len(col)) + 5
            worksheet.set_column(i, i, max_len)
    return output.getvalue()

# --- CARICAMENTO DATI ---
df_reps_db = load_sales_reps()
lista_nomi_reps = sorted(df_reps_db['Sales Representative'].unique())
df_all = load_mock_data(lista_nomi_reps)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<span class="sidebar-section-title">Seleziona Sales Representative</span>', unsafe_allow_html=True)
    sales_rep = st.selectbox("Seleziona Sales Representative", lista_nomi_reps, label_visibility="collapsed")

    st.markdown("---")

    st.markdown('<span class="sidebar-section-title">Seleziona Cliente</span>', unsafe_allow_html=True)
    df_rep_filtered = df_all[df_all['Sales Representative'] == sales_rep]
    nomi_clienti = sorted(df_rep_filtered['Nome Cliente'].unique())
    cliente_nome = st.selectbox("Seleziona Cliente", nomi_clienti, label_visibility="collapsed")

    cliente_codice = df_rep_filtered[df_rep_filtered['Nome Cliente'] == cliente_nome]['Codice Cliente'].iloc[0]
    df_display = df_rep_filtered[df_rep_filtered['Codice Cliente'] == cliente_codice].copy()

# --- CONTENUTO PRINCIPALE ---
st.markdown(f"""
    <div class="header-container">
        <img src="{LOGO_MAIN}" class="logo-img">
        <div>
            <h1 class="main-title">TEP: Tire Exchange Program</h1>
            <p class="sub-title">Gestione Resi Stagionali 2026</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write(f"**Cliente:** {cliente_nome} ({cliente_codice}) | **Sales Rep:** {sales_rep}")

if not df_display.empty:
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']].copy()
    rows = []
    for _, row in df_view.iterrows():
        qty_rest = row['Quantità restituibile']
        qty_cell = '<span style="color:#8899BB;">0</span>' if qty_rest == 0 else str(int(qty_rest))
        rows.append(f"<tr><td>{row['Size & Type']}</td><td>{int(row['Quantità Iniziale'])}</td><td>{qty_cell}</td></tr>")
    
    rows_html = "".join(rows)
    table_html = (
        f'<div style="overflow-x:auto;"><table class="tep-table">'
        f'<thead><tr><th>Pneumatico</th><th>Qtà Iniziale</th><th>Qtà Restituibile</th></tr></thead>'
        f'<tbody>{rows_html}</tbody></table></div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("---")
    excel_file = to_excel(df_view, cliente_codice, cliente_nome)
    nome_file = f"Restituzione_TEP_{cliente_codice}_{cliente_nome.replace(' ', '_')}.xlsx"
    st.download_button(
        label="📥 SCARICA MODULO DI RESO",
        data=excel_file,
        file_name=nome_file,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
