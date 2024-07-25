import streamlit as st
import pandas as pd
import numpy as np

class StreamlistSharing:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Nome Dipendente', 'Ore di Lavoro', 'Giorni Liberi'])
        self.orario_apertura = ""
        self.giorni_apertura = ""
        self.scheduling = None

    def aggiungi_dipendente(self, nome, ore, giorni_liberi):
        new_row = pd.DataFrame({'Nome Dipendente': [nome], 'Ore di Lavoro': [ore], 'Giorni Liberi': [giorni_liberi]})
        self.data = pd.concat([self.data, new_row], ignore_index=True)

    def mostra_streamlist(self):
        st.write(self.data)

    def totale_dipendenti(self):
        return len(self.data)

    def totale_ore_lavoro(self):
        return self.data['Ore di Lavoro'].sum()

    def imposta_orario_apertura(self, orario):
        self.orario_apertura = orario

    def imposta_giorni_apertura(self, giorni):
        self.giorni_apertura = giorni

    def mostra_info_negizio(self):
        st.write(f"Orario di apertura: {self.orario_apertura}")
        st.write(f"Giorni di apertura: {self.giorni_apertura}")

    def crea_scheduling(self):
        # Definire i parametri di base
        giorni = self.giorni_apertura.split('-')
        orario_inizio, orario_fine = map(int, self.orario_apertura.split('-'))
        ore_lavoro_settimanali = 40

        # Calcolare le ore di apertura giornaliere
        ore_apertura_giornaliera = orario_fine - orario_inizio
        ore_apertura_settimanale = ore_apertura_giornaliera * len(giorni)

        # Calcolare il numero di dipendenti necessari per coprire l'intera settimana
        numero_dipendenti = len(self.data)

        # Creare uno schedule vuoto
        schedule = pd.DataFrame(index=giorni, columns=[f'{orario_inizio + i}:00' for i in range(ore_apertura_giornaliera)])
        schedule[:] = np.nan

        # Assegnare le ore ai dipendenti
        for idx, row in self.data.iterrows():
            nome = row['Nome Dipendente']
            ore_rimanenti = ore_lavoro_settimanali
            giorni_liberi = row['Giorni Liberi'].split(',')
            for giorno in giorni:
                if giorno not in giorni_liberi:
                    for ora in range(orario_inizio, orario_fine):
                        if ore_rimanenti > 0 and pd.isna(schedule.at[giorno, f'{ora}:00']):
                            schedule.at[giorno, f'{ora}:00'] = nome
                            ore_rimanenti -= 1

        self.scheduling = schedule

    def mostra_scheduling(self):
        st.write(self.scheduling)

# Creazione dell'oggetto StreamlistSharing
streamlist = StreamlistSharing()

# Interfaccia Streamlit
st.title("Streamlist Sharing")

# Form per aggiungere dipendenti
st.header("Aggiungi Dipendenti")
giorni_settimana = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
for i in range(1, 9):
    with st.form(key=f'aggiungi_dipendente_{i}'):
        nome = st.text_input(f"Nome Dipendente {i}")
        ore = st.number_input(f"Ore di Lavoro {i}", min_value=0, max_value=100, step=1)
        giorni_liberi = []
        for giorno in giorni_settimana:
            if st.checkbox(f'{giorno} libero per Dipendente {i}'):
                giorni_liberi.append(giorno)
        giorni_liberi_str = ','.join(giorni_liberi)
        submit_button = st.form_submit_button(label=f'Aggiungi Dipendente {i}')

        if submit_button and nome:
            streamlist.aggiungi_dipendente(nome, ore, giorni_liberi_str)
            st.success(f"Dipendente {nome} aggiunto con {ore} ore di lavoro e giorni liberi: {giorni_liberi_str}")

# Form per impostare l'orario e i giorni di apertura
st.header("Imposta Orario e Giorni di Apertura")
with st.form(key='imposta_orario_giorni'):
    orario_apertura = st.text_input("Orario di Apertura (es. 10-24)")
    giorni_apertura = st.text_input("Giorni di Apertura (es. Lun-Mar-Mer-Gio-Ven-Sab-Dom)")
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
