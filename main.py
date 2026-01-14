import streamlit as st
import pandas as pd

# Configurações da Pagina
# Titulo da aba e icone da aba
st.set_page_config(page_title="Finanças", page_icon="💰")

st.markdown(
    """
# Boas vindas
# Ao nosso App
 Espero que você goste da nossa solção para organização de suas finanças.

    """
)

# Upload dos dados
file_uploader = st.file_uploader(label="Faça o upload dos dados !", type=["csv"])

if file_uploader:
    # Leitura dos dados
    df = pd.read_csv(file_uploader)
    columns_format = {"Valor":st.column_config.NumberColumn("Valor", format="R$ %f")}

    # Exeibição dos dados
    st.dataframe(df, hide_index=True, column_config=columns_format)