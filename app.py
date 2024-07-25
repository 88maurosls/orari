import streamlit as st
import pandas as pd

class StreamlistSharing:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Nome Dipendente', 'Ore di Lavoro'])
        self.orario_apertura = ""
        self.giorni_apertura = ""

    def aggiungi_dipendente(self, nome, ore):
        self.data = self.data.append({'Nome Dipendente': nome, 'Ore di Lavoro': ore}, ignore_index=True)

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

# Creazione dell'oggetto StreamlistSharing
streamlist = StreamlistSharing()

# Interfaccia Streamlit
st.title("Streamlist Sharing")

# Form per aggiungere dipendenti
st.header("Aggiungi Dipendenti")
for i in range(1, 9):
    with st.form(key=f'aggiungi_dipendente_{i}'):
        nome = st.text_input(f"Nome Dipendente {i}")
        ore = st.number_input(f"Ore di Lavoro {i}", min_value=0, max_value=100, step=1)
        submit_button = st.form_submit_button(label=f'Aggiungi Dipendente {i}')

        if submit_button and nome:
            streamlist.aggiungi_dipendente(nome, ore)
            st.success(f"Dipendente {nome} aggiunto con {ore} ore di lavoro")

# Form per impostare l'orario e i giorni di apertura
st.header("Imposta Orario e Giorni di Apertura")
with st.form(key='imposta_orario_giorni'):
    orario_apertura = st.text_input("Orario di Apertura (es. 9:00 - 18:00)")
    giorni_apertura = st.text_input("Giorni di Apertura (es. Lun-Ven)")
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
