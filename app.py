import streamlit as st
import pandas as pd
import numpy as np

class StreamlistSharing:
    def __init__(self):
        if 'data' not in st.session_state:
            st.session_state['data'] = pd.DataFrame(columns=['Nome Dipendente', 'Ore di Lavoro', 'Giorni Liberi'])
        if 'orario_apertura' not in st.session_state:
            st.session_state['orario_apertura'] = ""
        if 'giorni_apertura' not in st.session_state:
            st.session_state['giorni_apertura'] = ""
        if 'scheduling' not in st.session_state:
            st.session_state['scheduling'] = None

    def aggiungi_o_aggiorna_dipendente(self, idx, nome, ore, giorni_liberi):
        if idx < len(st.session_state['data']):
            st.session_state['data'].loc[idx] = [nome, ore, giorni_liberi]
        else:
            new_row = pd.DataFrame({'Nome Dipendente': [nome], 'Ore di Lavoro': [ore], 'Giorni Liberi': [giorni_liberi]})
            st.session_state['data'] = pd.concat([st.session_state['data'], new_row], ignore_index=True)

    def mostra_streamlist(self):
        st.write(st.session_state['data'])

    def totale_dipendenti(self):
        return len(st.session_state['data'])

    def totale_ore_lavoro(self):
        return st.session_state['data']['Ore di Lavoro'].sum()

    def imposta_orario_apertura(self, orario):
        st.session_state['orario_apertura'] = orario

    def imposta_giorni_apertura(self, giorni):
        st.session_state['giorni_apertura'] = giorni

    def mostra_info_negizio(self):
        st.write(f"Orario di apertura: {st.session_state['orario_apertura']}")
        st.write(f"Giorni di apertura: {st.session_state['giorni_apertura']}")

    def crea_scheduling(self):
        # Definire i parametri di base
        giorni = st.session_state['giorni_apertura'].split('-')
        orario_inizio, orario_fine = map(int, st.session_state['orario_apertura'].split('-'))
        ore_lavoro_settimanali = 40

        # Calcolare le ore di apertura giornaliere
        ore_apertura_giornaliera = orario_fine - orario_inizio
        ore_apertura_settimanale = ore_apertura_giornaliera * len(giorni)

        # Calcolare il numero di dipendenti necessari per coprire l'intera settimana
        numero_dipendenti = len(st.session_state['data'])

        # Creare uno schedule vuoto
        schedule = pd.DataFrame(index=giorni, columns=[f'{orario_inizio + i}:00' for i in range(ore_apertura_giornaliera)])
        schedule[:] = np.nan

        # Assegnare le ore ai dipendenti
        for idx, row in st.session_state['data'].iterrows():
            nome = row['Nome Dipendente']
            ore_rimanenti = ore_lavoro_settimanali
            giorni_liberi = row['Giorni Liberi'].split(',')
            for giorno in giorni:
                if giorno not in giorni_liberi:
                    for ora in range(orario_inizio, orario_fine):
                        if ore_rimanenti > 0 and pd.isna(schedule.at[giorno, f'{ora}:00']):
                            schedule.at[giorno, f'{ora}:00'] = nome
                            ore_rimanenti -= 1

        st.session_state['scheduling'] = schedule

    def mostra_scheduling(self):
        st.write(st.session_state['scheduling'])

# Creazione dell'oggetto StreamlistSharing
streamlist = StreamlistSharing()

# Interfaccia Streamlit
st.title("Streamlist Sharing")

# Form per aggiungere o aggiornare dipendenti
st.header("Aggiungi o Aggiorna Dipendenti")
giorni_settimana = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
for i in range(8):
    with st.form(key=f'aggiungi_dipendente_{i}'):
        nome = st.text_input(f"Nome Dipendente {i + 1}", value=st.session_state['data'].iloc[i]['Nome Dipendente'] if i < len(st.session_state['data']) else "")
        ore = st.number_input(f"Ore di Lavoro {i + 1}", min_value=0, max_value=100, step=1, value=st.session_state['data'].iloc[i]['Ore di Lavoro'] if i < len(st.session_state['data']) else 0)
        giorni_liberi = []
        cols = st.columns(7)
        for j, giorno in enumerate(giorni_settimana):
            with cols[j]:
                if st.checkbox(f'{giorno}', value=giorno in st.session_state['data'].iloc[i]['Giorni Liberi'].split(',') if i < len(st.session_state['data']) else False):
                    giorni_liberi.append(giorno)
        giorni_liberi_str = ','.join(giorni_liberi)
        submit_button = st.form_submit_button(label=f'Salva Dipendente {i + 1}')

        if submit_button and nome:
            streamlist.aggiungi_o_aggiorna_dipendente(i, nome, ore, giorni_liberi_str)
            st.success(f"Dati del dipendente {i + 1} salvati")

# Form per impostare l'orario e i giorni di apertura
st.header("Imposta Orario e Giorni di Apertura")
with st.form(key='imposta_orario_giorni'):
    orario_apertura = st.text_input("Orario di Apertura (es. 10-24)", value=st.session_state['orario_apertura'])
    giorni_apertura = st.text_input("Giorni di Apertura (es. Lun-Mar-Mer-Gio-Ven-Sab-Dom)", value=st.session_state['giorni_apertura'])
    submit_button = st.form_submit_button(label='Imposta Orario e Giorni di Apertura')

    if submit_button:
        streamlist.imposta_orario_apertura(orario_apertura)
        streamlist.imposta_giorni_apertura(giorni_apertura)
        st.success("Orario e giorni di apertura impostati")

# Mostra streamlist attuale
st.header("Streamlist Attuale")
streamlist.mostra_streamlist()

# Mostra totale dipendenti e ore di lavoro
st.header("Totali")
st.write(f"Numero totale di dipendenti: {streamlist.totale_dipendenti()}")
st.write(f"Totale ore di lavoro: {streamlist.totale_ore_lavoro()}")

# Mostra informazioni sul negozio
st.header("Informazioni sul Negozio")
streamlist.mostra_info_negizio()

# Creazione e visualizzazione dello scheduling
if st.button('Crea Scheduling'):
    streamlist.crea_scheduling()
    st.header("Scheduling Settimanale")
    streamlist.mostra_scheduling()
