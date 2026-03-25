import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title='Dashboard de filmes avaliados pelo IMDB',
    page_icon='🎬',
    layout='wide'
)

df = pd.read_csv('filmes.csv')

st.sidebar.header('🔍 Filtros')

df['genero'] = df['genero'].str.split(', ')

generos = sorted(set(g for lista in df['genero'] for g in lista))
genero_selecionado = st.sidebar.multiselect('Gêneros', generos, default=generos)

ano_min, ano_max = int(df['ano'].min()), int(df['ano'].max())
ano_selecionado = st.sidebar.slider('Ano de lançamento', ano_min, ano_max, (ano_min, ano_max))

classificacao_disponivel = sorted(df['classificação indicativa'].unique())
classificacao_selecionada = st.sidebar.multiselect('classificação indicativa', classificacao_disponivel, default=classificacao_disponivel)

filtro_genero = df['genero'].apply(
    lambda lista: any(g in lista for g in genero_selecionado)
)

df_filtrado = df[
    filtro_genero &
    (df['ano'] >= ano_selecionado[0]) &
    (df['ano'] <= ano_selecionado[1]) &
    (df['classificação indicativa'].isin(classificacao_selecionada))
]

media = df_filtrado['bilheteria total(USD)'].mean() / 1_000_000

st.title('🎬 Dashboard de filmes avaliados pelo IMDB')

col1, col2, col3, col4 = st.columns(4)

col1.metric('💰 Bilheteria média', f'${media:.1f}M')
col2.metric('⭐ Nota média', round(df_filtrado['nota IMDB'].mean()))
col3.metric('🎬 Total de filmes', df_filtrado.shape[0])
col4.metric('🗳️ Média de votos', round(df_filtrado['numero de votos'].mean()))

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        st.subheader('💰 Relação entre bilheteria e nota')

        fig1 = px.scatter(
            df_filtrado,
            x='nota IMDB',
            y='bilheteria total(USD)'
        )

        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning('Não há dados para exibir no gráfico')

with col_graf2:
    if not df_filtrado.empty:
        st.subheader('🎭 Gêneros mais lucrativos')

        df_gen = df_filtrado.explode('genero')

        df_lucro = (df_gen.groupby('genero')['bilheteria total(USD)'].mean().sort_values(ascending=False).reset_index())

        fig2 = px.bar(
            df_lucro,
            x='genero',
            y='bilheteria total(USD)'
        )

        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning('Não há dados para exibir no gráfico')


col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        st.subheader('🔞 Impacto da classificação na bilheteria')

        df_classificacao = df_filtrado.groupby('classificação indicativa')['bilheteria total(USD)'].mean().sort_values(ascending=False).reset_index()

        fig3 = px.bar(
            df_classificacao,
            x='classificação indicativa',
            y='bilheteria total(USD)'
        )

        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning('Não há dados para exibir no gráfico')

with col_graf4:
    if not df_filtrado.empty:
        st.subheader('📅 Média das notas ao longo dos anos')

        df_anos = df_filtrado.groupby('nota IMDB')['ano'].mean().sort_values(ascending=False).reset_index()

        fig4 = px.line(
            df_anos,
            x='nota IMDB',
            y='ano'
        )

        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning('Não há dados para exibir no gráfico')


st.subheader('Dados utilizados')
st.dataframe(df_filtrado)