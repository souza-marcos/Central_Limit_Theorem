import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Função para gerar amostrar do tipo de distribuição escolhido
def gerar_amostras(tipo_distr, params, tam_amostra : int, num_amostras : int):
    if tipo_distr == 'Binomial':
        return np.random.binomial(params['n'], params['p'], size=(num_amostras, tam_amostra))
    elif tipo_distr == 'Exponencial':
        return np.random.exponential(scale=params['lambda'], size=(num_amostras, tam_amostra))
    elif tipo_distr == 'Uniforme':
        return np.random.uniform(params['a'], params['b'], size=(num_amostras, tam_amostra))
    elif tipo_distr == 'Poisson':
        return np.random.poisson(params['lambda'], size=(num_amostras, tam_amostra))

# Função para calcular médias amostrais
def calcular_medias_amostrais(amostras):
    return np.mean(amostras, axis=1)

# Função para plotar histogramas
def plotar_histograma(axe_index, data, titulo, color, type):
    axes[axe_index].hist(data, bins=15, alpha=0.7, color=color, edgecolor='black')
    axes[axe_index].set_title(titulo)
    if(type == 'Valores'):
        axes[axe_index].set_xlabel("Valor da amostra")
        axes[axe_index].set_ylabel("Número de amostras")
    if(type == 'Médias'):
        axes[axe_index].set_xlabel("Valor médio do conjunto de amostras")
        axes[axe_index].set_ylabel("Número de conjuntos de amostras")

# Função para plotar distribuição normal sobreposta
def plotar_normal(medias_amostrais, media_real, desvio_padrao_real):
    x = np.linspace(min(medias_amostrais), max(medias_amostrais), 100)
    # x = np.linspace(norm.ppf(1), norm.ppf(100), 100)
    # y_normal = norm.pdf(x, loc=media_real, scale=desvio_padrao_real)
    rv = norm(loc = media_real, scale = desvio_padrao_real)
    y_normal = rv.pdf(x)

    ax3 = axes[1].twinx()

    ax3.plot(x, y_normal, 'k--', linewidth=2, label='Distribuição Normal')
    #ax3.set_ylabel('Distribuição Normal', color='k')
    ax3.tick_params(axis='y', labelcolor='k')
    
# Função principal
def main():
    st.set_page_config(layout="wide")
    st.write("# Prova 3 - Probabilidade - EST032")
    st.write("### Alunos:")
    st.write("##### Marcos Daniel Souza Netto - 2022069492")
    st.write("##### Gustavo Chaves Ferreira - 2022043329")
    st.divider()
    _ , col2, _ = st.columns([1, 1, 1])
    with col2:
        st.write("## Teorema Central do Limite")
    st.write("O Teorema Central do Limite, também conhecido como TCL, é um dos resultados mais importantes no campo da teoria das probabilidades. De modo geral, ele afirma que, tomadas amostras suficientemente grandes de uma população, a média de tais amostras apresentará uma distribuição aproximadamente normal, ainda que a população em questão não seja normalmente distribuída.")
    st.write("O objetivo desta aplicação é mostrar esse princípio sendo aplicado na prática! Uma vez selecionado uma distruibuição e tamanhos para as amostras, você poderá perceber, através dos gráficos abaixo, que o formato do histograma das médias se aproxima da curva normal à medida que o número de amostras cresce.")
    st.write("Fique à vontade para personalizar os parâmetros e observar os resultados!")
    st.divider()    

    # Escolher distribuição e parâmetros
    tipo_distribuicao = st.selectbox("Escolha o tipo de distribuição:", ["Binomial", "Exponencial", "Uniforme", "Poisson"])
    parametros = {}

    st.write("###")

    st.write("Escolha os parâmetros da distribuição selecionada:")
    
    if tipo_distribuicao == 'Binomial':
        parametros['n'] = st.slider("Número de tentativas (n)", min_value=5, max_value=50, value=20)
        parametros['p'] = st.slider("Probabilidade de sucesso (p)", min_value=0.01, max_value=0.9, value=0.5)
    elif tipo_distribuicao == 'Exponencial':
        parametros['lambda'] = st.slider("Parâmetro Lambda", min_value=0.1, max_value=5.0, value=1.0)
    elif tipo_distribuicao == 'Uniforme':
        parametros['a'] = st.slider("Limite inferior (a)", min_value=0, max_value=10, value=0)
        parametros['b'] = st.slider("Limite superior (b)", min_value=10, max_value=20, value=10)
    elif tipo_distribuicao == 'Poisson':
        parametros['lambda'] = st.slider("Parâmetro Lambda", min_value=0.1, max_value=5.0, value=1.0)
    
    st.write("###")

    st.write("Escolha os valores das amostras:")
        
    tamanho_amostra = st.slider("Tamanho da Amostra", min_value=5, max_value=100, value=30)
    num_amostras = st.slider("Número de Amostras", min_value=1, max_value=1000, value=10)

    # Gerar amostras
    amostras = gerar_amostras(tipo_distribuicao, parametros, tamanho_amostra, num_amostras)

    # Calcular médias amostrais
    medias_amostrais = calcular_medias_amostrais(amostras)

    # Plotar histograma das amostras
    plotar_histograma(
        0,
        amostras.flatten(),
        f'Distribuição das Amostras ({tipo_distribuicao})',
        'b',
        'Valores'
    )

    # Plotar histograma das médias amostrais
    plotar_histograma(
        1,
        medias_amostrais,
        f'Distribuição das Médias Amostrais ({tipo_distribuicao})',
        'r',
        'Médias'
    )

    # Plotar distribuição normal sobreposta
    media_real = np.mean(amostras)
    desvio_padrao_real = np.std(amostras) / np.sqrt(tamanho_amostra)
    plotar_normal(medias_amostrais, media_real, desvio_padrao_real)

    plt.subplots_adjust(wspace=0.3)
    st.pyplot(fig)

# Executar o programa principal
if __name__ == "__main__":
    main()
