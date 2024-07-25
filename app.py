import streamlit as st
import pandas as pd
import numpy as np

class StreamlistSharing:
    def __init__(self):
        if 'data' not in st.session_state:
            st.session_state['data'] = pd.DataFrame(columns=['Nome Dipendente', 'Ore di Lavoro', 'Giorni Liberi', 'Ore Extra'])
        if 'orario_apertura' not in st.session_state:
            st.session_state['orario_apertura'] = ""
        if 'giorni_apertura' not in st.session_state:
            st.session_state['giorni_apertura'] = ""
        if 'scheduling' not in st.session_state:
            st.session_state['scheduling'] = None
        if 'num_dipendenti' not in st.session_state:
            st.session_state['num_dipendenti'] = 6  # Numero di dipendenti iniziali di default
        if 'fasce_orarie' not in st.session_state:
            st.session_state['fasce_orarie'] = pd.DataFrame(columns=['Inizio', 'Fine', 'Minimo Dipendenti'])

    def aggiungi_o_aggiorna_dipendente(self, idx, nome, ore, giorni_liberi):
        if idx < len(st.session_state['data']):
            st.session_state['data'].loc[idx] = [nome, ore, giorni_liberi, 0]
        else:
            new_row = pd.DataFrame({'Nome Dipendente': [nome], 'Ore di Lavoro': [ore], 'Giorni Liberi': [giorni_liberi], 'Ore Extra': [0]})
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

    def imposta_fasce_orarie(self, fasce):
        st.session_state['fasce_orarie'] = pd.DataFrame(fasce)

    def mostra_info_negizio(self):
        st.write(f"Orario di apertura: {st.session_state['orario_apertura']}")
        st.write(f"Giorni di apertura: {st.session_state['giorni_apertura']}")
        st.write("Fasce orarie e minimo dipendenti:")
        st.write(st.session_state['fasce_orarie'])

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

        # Assegnare le ore ai dipendenti rispettando il minimo per fascia oraria
        fasce_orarie = st.session_state['fasce_orarie']
        for giorno in giorni:
            for _, fascia in fasce_orarie.iterrows():
                inizio, fine, minimo_dipendenti = fascia['Inizio'], fascia['Fine'], fascia['Minimo Dipendenti']
                for ora in range(inizio, fine):
                    dipendenti_assegnati = 0
                    for idx, row in st.session_state['data'].iterrows():
                        nome = row['Nome Dipendente']
                        ore_rimanenti = row['Ore di Lavoro']
                        giorni_liberi = row['Giorni Liberi'].split(',')
                        if giorno not in giorni_liberi and ore_rimanenti > 0:
                            if pd.isna(schedule.at[giorno, f'{ora}:00']):
                                schedule.at[giorno, f'{ora}:00'] = nome
                                st.session_state['data'].at[idx, 'Ore di Lavoro'] -= 1
                                dipendenti_assegnati += 1
                            elif isinstance(schedule.at[giorno, f'{ora}:00'], str) and nome not in schedule.at[giorno, f'{ora}:00']:
                                schedule.at[giorno, f'{ora}:00'] += f', {nome}'
                                st.session_state['data'].at[idx, 'Ore di Lavoro'] -= 1
                                dipendenti_assegnati += 1
                            if dipendenti_assegnati >= minimo_dipendenti:
                                break
                    if dipendenti_assegnati < minimo_dipendenti:
                        st.warning(f"Non ci sono abbastanza dipendenti per coprire la fascia oraria {inizio}-{fine} di {giorno}")
                        for idx, row in st.session_state['data'].iterrows():
                            nome = row['Nome Dipendente']
                            giorni_liberi = row['Giorni Liberi'].split(',')
                            if giorno not in giorni_liberi:
                                if pd.isna(schedule.at[giorno, f'{ora}:00']) or nome not in schedule.at[giorno, f'{ora}:00']:
                                    if pd.notna(schedule.at[giorno, f'{ora}:00']):
                                        schedule.at[giorno, f'{ora}:00'] += f', {nome}'
                                    else:
                                        schedule.at[giorno, f'{ora}:00'] = nome
                                    st.session_state['data'].at[idx, 'Ore Extra'] += 1
                                    dipendenti_assegnati += 1
                                if dipendenti_assegnati >= minimo_dipendenti:
                                    break

        st.session_state['scheduling'] = schedule

    def mostra_scheduling(self):
        st.write(st.session_state['scheduling'])
        st.write("Ore Extra Settimanali per Dipendente:")
        st.write(st.session_state['data'][['Nome Dipendente', 'Ore Extra']])

# Creazione dell'oggetto StreamlistSharing
streamlist = StreamlistSharing()

# Interfaccia Streamlit
st.title("Streamlist Sharing")

# Form per aggiungere o aggiornare dipendenti
st.header("Aggiungi o Aggiorna Dipendenti")
giorni_settimana = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']

for i in range(st.session_state['num_dipendenti']):
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

# Pulsante per aggiungere più dipendenti
if st.button('Aggiungi Dipendente'):
    st.session_state['num_dipendenti'] += 1

# Form per impostare l'orario e i giorni di apertura
st.header("Imposta Orario e Giorni di Apertura")
with st.form(key='imposta_orario_giorni'):
    orario_apertura = st.text_input("Orario di Apertura (es. 10-24)", value=st.session_state['orario_apertura'])
    giorni_apertura = st.text_input("Giorni di Apertura (es. Lun-Mar-Mer-Gio-Ven-Sab-Dom)", value=st.session_state['giorni_apertura'])
    
    fasce_orarie = []
    for i in range(3):
        col1, col2, col3 = st.columns(3)
        with col1:
            inizio = st.number_input(f'Inizio Fascia {i+1}', min_value=0, max_value=24, value=10 if i == 0 else (16 if i == 1 else 22))
        with col2:
            fine = st.number_input(f'Fine Fascia {i+1}', min_value=0, max_value=24, value=16 if i == 0 else (22 if i == 1 else 24))
        with col3:
            minimo_dipendenti = st.number_input(f'Minimo Dipendenti Fascia {i+1}', min_value=0, max_value=20, value=2)
        fasce_orarie.append({'Inizio': inizio, 'Fine': fine, 'Minimo Dipendenti': minimo_dipendenti})
    
    submit_button = st.form_submit_button(label='Imposta Orario e Giorni di Apertura')

    if submit_button:
        streamlist.imposta_orario_apertura(orario_apertura)
        streamlist.imposta_giorni_apertura(giorni_apertura)
        streamlist.imposta_fasce_orarie(fasce_orarie)
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
