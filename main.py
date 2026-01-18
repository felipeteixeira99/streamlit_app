import streamlit as st
import pandas as pd

def estatisticas_gerais(df:pd.DataFrame):
    df_data = df.groupby(by="Data")[["Valor"]].sum()

    # Cria uma nova coluna deslocando valores para baixo
    df_data['lag_1'] = df_data['Valor'].shift(1)
    df_data['Diferença Mensal Abs.'] = df_data['Valor'] - df_data['lag_1']
    # Médias moveis
    df_data['Media 6M Diferença Mensal Abs.'] = df_data["Diferença Mensal Abs."].rolling(6).mean()
    df_data['Media 12M Diferença Mensal Abs.'] = df_data["Diferença Mensal Abs."].rolling(12).mean()
    df_data['Media 24M Diferença Mensal Abs.'] = df_data["Diferença Mensal Abs."].rolling(24).mean()

    df_data['Diferença Mensal Rel.'] = df_data['Valor'] / df_data['lag_1'] - 1

    # Evolucao dos x meses
    df_data["Evolução 6M Total"] = df_data["Valor"].rolling(6).apply(lambda x: x[-1] - x[0])
    df_data["Evolução 12M Total"] = df_data["Valor"].rolling(12).apply(lambda x: x[-1] - x[0])
    df_data["Evolução 24M Total"] = df_data["Valor"].rolling(24).apply(lambda x: x[-1] - x[0])

    df_data["Evolução 6M Relativa"] = df_data["Valor"].rolling(6).apply(lambda x: x[-1] / x[0] - 1 ) 
    df_data["Evolução 12M Relativa"] = df_data["Valor"].rolling(12).apply(lambda x: x[-1] / x[0] - 1 )
    df_data["Evolução 24M Relativa"] = df_data["Valor"].rolling(24).apply(lambda x: x[-1] / x[0] - 1 )

    # Dropa Coluna lag_1
    df_data = df_data.drop('lag_1', axis=1)

    return df_data

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
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

    columns_format = {"Valor":st.column_config.NumberColumn("Valor", format="R$ %f")}

    # Exeibição dos dados
    exp1 = st.expander("Dados Brutos")
    exp1.dataframe(df, hide_index=True, column_config=columns_format)

    # Visão Instituição
    exp2 = st.expander("Instituições")

    df_instituicao = df.pivot(index="Data", columns="Instituição", values="Valor")

    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Historico", "Distribuição"])

    with tab_data:
        st.dataframe(df_instituicao)

    #exp2.dataframe(df_instituicao)
    # Grafico
    with tab_history:
        st.line_chart(df_instituicao)

    # Ultima data com dados
    with tab_share:

        date = st.date_input("Data para Distribuição", 
                    min_value=df_instituicao.index.min(),
                    max_value=df_instituicao.index.max())
        if date not in df_instituicao.index:
            st.warning("Entre com uma data válida")

        else:
            st.bar_chart(df_instituicao.loc[date])
    
    exp3 = st.expander("Estatisticas Gerais")
 
    df_stats = estatisticas_gerais(df)

    columns_config = {
    'Valor': st.column_config.NumberColumn('Valor', format= "R$ %.2f"), 
    'Diferença Mensal Abs.': st.column_config.NumberColumn('Diferença Mensal Abs.', format= "R$ %.2f"), 
    'Media 6M Diferença Mensal Abs.': st.column_config.NumberColumn('Media 6M Diferença Mensal Abs.', format= "R$ %.2f"), 
    'Media 12M Diferença Mensal Abs.': st.column_config.NumberColumn('Media 12M Diferença Mensal Abs.', format= "R$ %.2f"), 
    'Media 24M Diferença Mensal Abs.': st.column_config.NumberColumn('Media 24M Diferença Mensal Abs.', format= "R$ %.2f"), 
    'Evolução 6M Total': st.column_config.NumberColumn('Evolução 6M Total', format= "R$ %.2f"), 
    'Evolução 12M Total': st.column_config.NumberColumn('Evolução 12M Total', format= "R$ %.2f"), 
    'Evolução 24M Total': st.column_config.NumberColumn('Evolução 24M Total', format= "R$ %.2f"), 
    'Diferença Mensal Rel.': st.column_config.NumberColumn("'Diferença Mensal Rel.", format="percent"),
    'Evolução 6M Relativa': st.column_config.NumberColumn(" 'Evolução 6M Relativa", format="percent"),
    'Evolução 12M Relativa': st.column_config.NumberColumn("'Evolução 12M Relativa", format="percent"),
    'Evolução 24M Relativa': st.column_config.NumberColumn("'Evolução 24M Relativa", format="percent")
    }

    tab_stats, tab_abs, tab_rel = exp3.tabs(tabs=["Dados", "Historico de Evolução", "Crescimento Relativo"])
    
    with tab_abs:
        abs_cols = [
        'Diferença Mensal Abs.',
        'Media 6M Diferença Mensal Abs.',
        'Media 12M Diferença Mensal Abs.',
        'Media 24M Diferença Mensal Abs.'
        ]
        st.line_chart(df_stats[abs_cols])
        

    with tab_stats: 
        st.dataframe(df_stats, column_config=columns_config)


    with tab_rel:
        rel_cols = [
            'Diferença Mensal Rel.',
            'Evolução 6M Relativa',
            'Evolução 12M Relativa',
            'Evolução 24M Relativa',
        ]
        st.line_chart(data=df_stats[rel_cols])

    with st.expander("Metas"):

        col1, col2 = st.columns(2)

        data_inicio_meta = col1.date_input("Inicio da Meta", max_value=df_stats.index.max())

        filter_data = df_stats.index <= data_inicio_meta
        data_filtrada = df_stats.index[filter_data][-1]


        # valor_inicio = df_stats.loc[data_filtrada]["Valor"]
        # col2.markdown(f"**Valor No Inicio da Meta**: R$ {valor_inicio:.2f}")
    
        salario_bruto = col2.number_input("Salário Bruto", min_value=0., format="%.2f")
        salario_liquido = col2.number_input("Salário Liquido", min_value=0., format="%.2f")
        custos_fixos = col1.number_input("Custos Fixos", min_value=0., format="%.2f")

        valor_inicio = df_stats.loc[data_filtrada]["Valor"]
        st.markdown(f"**Valor No Inicio da Meta**: R$ {valor_inicio:.2f}")

        col1_pot, col2_pot = st.columns(2)
        mensal = salario_liquido - custos_fixos
        anual = mensal * 12
        

        with col1.container(border=True):
            st.markdown(f"**Potencial Arrecadação Mês**: R$ {mensal:.2f}")

        with col2.container(border=True):
            st.markdown(f"**Potencial Arrecadação Anual**: R$ {anual:.2f}")

        #st.number_input("Meta Estipulada", min_value=0., format="%.2f", value=anual)

        with st.container(border=True):
            col1_meta, col2_meta = st.columns(2)
            with col1_meta:
                meta_estipulada =  st.number_input("Meta Estipulada", min_value=0., format="%.2f", value=anual)

            with col2_meta:
                patrimonio_final = meta_estipulada + valor_inicio
                st.markdown(f"Patrimonio Estimando pós meta: \n\n R$ {patrimonio_final:.2f}")


    