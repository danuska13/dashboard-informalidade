import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
page_title="Dashboard de Dados",
layout="wide"
)
st.title("Dashboard de Dados")
st.write("""
Este dashboard apresenta uma análise sobre informalidade no trabalho entre mulheres no Brasil.
""")
st.write("""<h2 style='color:#FF69B4;'>Feito por: Paola e Dani</h2>""",
            unsafe_allow_html=True)
st.caption("Fonte: dados.gov.br")

arquivo = st.file_uploader(
"Envie um arquivo CSV",
type=["csv"]
)
if arquivo is not None:
    df = pd.read_csv(arquivo,
                  sep=";",
                  encoding="utf-8-sig",
                  skiprows=1,
                  decimal=","
                 )
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    st.write("Colunas:", df.columns.tolist())
    st.write("Índice:", df.index)
    
    st.subheader("Visualização dos dados")
    st.dataframe(df.head())
    col1, col2 = st.columns(2)
    col1.metric(
    "Quantidade de registros",
    df.shape[0]
    )
    col2.metric("Quantidade de colunas",
    df.shape[1]
    )
    colunas_trimestre = df.columns[3:]
    df[colunas_trimestre] = df[colunas_trimestre].astype(float)

    # Tratamento 2: wide -> long, pronto pra gráfico
    df_long = df.melt(
        id_vars=["Sigla", "Código", "Brasil"],
        value_vars=colunas_trimestre,
        var_name="Trimestre",
        value_name="Informalidade"
    )

    # Tratamento 3: checar valores ausentes
    st.write("Valores ausentes:", df_long["Informalidade"].isnull().sum())
    st.write("Registros duplicados:", df.duplicated().sum())
    st.write("Tipos de dados (após tratamento):", df.dtypes)

    # Gráfico de linha com a série histórica
    st.subheader("Evolução da informalidade")
    fig = px.line(
        df_long,
        x="Trimestre",
        y="Informalidade",
        color="Sigla",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

  # Gráfico de coluna (barras) com a série histórica
    st.subheader("Informalidade por trimestre (colunas)")
    fig_bar = px.bar(
        df_long,
        x="Trimestre",
        y="Informalidade",
        color="Sigla",
        text="Informalidade"
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    # Cálculo automático do maior e menor valor 
    maior = df_long.loc[df_long["Informalidade"].idxmax()]
    menor = df_long.loc[df_long["Informalidade"].idxmin()]

    st.subheader("Perguntas")
    st.markdown("**Quais trimestres apresentam os maiores e menores valores?**")
    st.markdown(f"2019 e inicio de 2022")
    st.markdown("**Como os valores mudaram ao longo dos anos?**")
    st.markdown("em 2015 a 2019 houve uma subida gradual, em 2020 queda brusca, 2021-2022 recuperação e de 2023 em diante teve estabilização")

#indicador
    media = df_long["Informalidade"].mean()

    st.metric(
    "Valor médio",
    round(media, 2)
    )

#Explicação
    st.markdown("""
    ### O que podemos observar?
    Este gráfico mostra a evolução da taxa de informalidade no trabalho entre mulheres no Brasil, do último trimestre de 2015 até o primeiro trimestre de 2025, com valores medidos a cada trimestre. Ao longo desse período, a taxa oscilou principalmente entre 36% e 39,6%, com uma tendência geral de leve alta até 2019. O maior valor da série aparece no terceiro trimestre de 2019 (39,6%), e o menor valor ocorre no segundo trimestre de 2020 (34,5%), justamente no início da pandemia — uma queda bem mais acentuada que qualquer outra variação do período.

    Depois dessa queda em 2020, a taxa voltou a subir de forma consistente e, desde 2021, se estabilizou numa faixa entre 36% e 38,7%, sem grandes variações. Vale destacar que o gráfico mostra apenas a variação ao longo do tempo — ele não indica os motivos por trás dessas mudanças, apenas que elas aconteceram.
    """)

#Respondendo perguntas finais
    st.markdown("""
        <h2 style='color:#FF69B4;'> – Exemplo de uso da IA</h2>

        **Problema:** o CSV tava carregando tudo errado no pandas — aparecia só 1 coluna quando na verdade tinha um monte.

        **Prompt:** mandamos print do código e do erro e perguntamos pra IA se aquilo fazia sentido.

        **Sugestão da IA:** fomos achando os problemas um por um: primeiro o encoding errado, depois um bug no índice que tava "comendo" as colunas, e no final descobriu que tinha uma linha de título sobrando no CSV.

        **O que fizemos:** fomos testando cada correção separada, vendo se dava certo antes de seguir pra próxima. Também rolou de ajustar o decimal (vírgula vs ponto), que só apareceu depois.

        **Como conferimos:** batemos o número de colunas que apareceu (41) com o que realmente tinha no arquivo, e vimos se os números finalmente viraram número de verdade (não texto).
        """, unsafe_allow_html=True)