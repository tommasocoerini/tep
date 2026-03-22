# --- AGGIORNA LA FUNZIONE TO_EXCEL CON LA NUOVA FORMATTAZIONE ---
def to_excel(df, codice, ragione_sociale):
    output = io.BytesIO()
    # Usiamo xlsxwriter per avere il controllo totale del layout
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reso_TEP', startrow=3)
        
        workbook  = writer.book
        worksheet = writer.sheets['Reso_TEP']

        # DEFINIZIONE FORMATI
        fmt_header = workbook.add_format({
            'bold': True,
            'bg_color': '#D3D3D3', # Grigio chiaro
            'border': 1,
            'align': 'center'
        })
        
        fmt_label = workbook.add_format({
            'bold': True,
            'bg_color': '#D3D3D3', # Grigio chiaro
            'border': 1
        })

        fmt_data_bold = workbook.add_format({'bold': True})

        # 1. INTESTAZIONE PERSONALIZZATA (Righe 1 e 2)
        worksheet.write('A1', 'CODICE CLIENTE', fmt_label)
        worksheet.write('B1', codice) # Il codice cliente
        
        worksheet.write('A2', 'RAGIONE SOCIALE', fmt_label)
        worksheet.write('B2', ragione_sociale, fmt_label) # Ragione sociale grigia e grassetto come richiesto

        # 2. FORMATTAZIONE INTESTAZIONI TABELLA (Riga 3 - indice 2 di Excel)
        # Sovrascriviamo le intestazioni create da pandas per dare lo stile grigio
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(2, col_num, value, fmt_header)

        # 3. AUTO-ADATTAMENTO LARGHEZZA COLONNE
        for i, col in enumerate(df.columns):
            # Calcola la lunghezza massima tra nome colonna e contenuto
            column_len = max(df[col].astype(str).map(len).max(), len(col)) + 5
            worksheet.set_column(i, i, column_len)

    return output.getvalue()

# --- NEL MAIN, MODIFICA LA CHIAMATA ALLA FUNZIONE ---
if not df_display.empty:
    df_view = df_display[['Size & Type', 'Quantità Iniziale', 'Quantità restituibile']].copy()

    # ... (qui tieni il codice della tabella HTML per la visione a schermo) ...
    
    st.markdown("---")
    
    # Passiamo anche il codice e il nome alla funzione excel
    excel_data = to_excel(df_view, cliente_codice, cliente_nome)
    
    st.download_button(
        label="📥 SCARICA MODULO DI RESO",
        data=excel_data,
        file_name=f"Modulo_Reso_{cliente_codice}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
