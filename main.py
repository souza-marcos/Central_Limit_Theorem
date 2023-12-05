import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

def gerar_amostras(tipo_distr, params, tam_amostra : int, num_amostras : int):
    if tipo_distr == 'Binomial':
        return np.random.binomial(params['n'], params['p'], size=(num_amostras, tam_amostra))
    elif tipo_distr == 'Exponencial':
        return np.random.exponential(scale=params['lambda'], size=(num_amostras, tam_amostra))
    elif tipo_distr == 'Uniforme':
        return np.random.uniform(params['a'], params['b'], size=(num_amostras, tam_amostra))

# Função para calcular médias amostrais
def calcular_medias_amostrais(amostras):
    return np.mean(amostras, axis=1)

# Função para plotar histogramas
def plotar_histograma(axe_index, data, titulo, color):
    axes[axe_index].hist(data, bins=20, alpha=0.7, color=color, edgecolor='black')
    axes[axe_index].set_title(titulo)

# Função para plotar distribuição normal sobreposta
def plotar_normal(medias_amostrais, media_real, desvio_padrao_real):
    x = np.linspace(min(medias_amostrais), max(medias_amostrais), 100)
    # x = np.linspace(norm.ppf(1), norm.ppf(100), 100)
    # y_normal = norm.pdf(x, loc=media_real, scale=desvio_padrao_real)
    rv = norm(loc = media_real, scale = desvio_padrao_real)
    y_normal = rv.pdf(x)

    ax3 = axes[1].twinx()

    ax3.plot(x, y_normal, 'k--', linewidth=2, label='Distribuição Normal')
    
    ax3.set_ylabel('Distribuição Normal', color='k')
    ax3.tick_params(axis='y', labelcolor='k')
    
# Função principal
def main():
    st.title("Teorema Central do Limite")

    # Escolher distribuição e parâmetros
    tipo_distribuicao = st.sidebar.selectbox("Escolha a Distribuição", ["Binomial", "Exponencial", "Uniforme"])
    parametros = {}

    if tipo_distribuicao == 'Binomial':
        st.sidebar.markdown("Parâmetros da Distribuição Binomial")
        parametros['n'] = st.sidebar.slider("Número de tentativas (n)", min_value=5, max_value=50, value=20)
        parametros['p'] = st.sidebar.slider("Probabilidade de sucesso (p)", min_value=0.1, max_value=0.9, value=0.5)
    elif tipo_distribuicao == 'Exponencial':
        st.sidebar.markdown("Parâmetros da Distribuição Exponencial")
        parametros['lambda'] = st.sidebar.slider("Parâmetro Lambda", min_value=0.1, max_value=5.0, value=1.0)
    elif tipo_distribuicao == 'Uniforme':
        st.sidebar.markdown("Parâmetros da Distribuição Uniforme")
        parametros['a'] = st.sidebar.slider("Limite inferior (a)", min_value=0, max_value=10, value=0)
        parametros['b'] = st.sidebar.slider("Limite superior (b)", min_value=10, max_value=20, value=10)

    tamanho_amostra = st.sidebar.slider("Tamanho da Amostra", min_value=5, max_value=100, value=30)
    num_amostras = st.sidebar.slider("Número de Amostras", min_value=1, max_value=1000, value=10)

    # Gerar amostras
    amostras = gerar_amostras(tipo_distribuicao, parametros, tamanho_amostra, num_amostras)

    # Calcular médias amostrais
    medias_amostrais = calcular_medias_amostrais(amostras)

    # Plotar histograma das amostras
    plotar_histograma(
        0,
        amostras.flatten(),
        f'Distribuição das Amostras ({tipo_distribuicao})',
        'b'
    )

    # Plotar histograma das médias amostrais
    plotar_histograma(
        1,
        medias_amostrais,
        f'Distribuição das Médias Amostrais ({tipo_distribuicao})',
        'r'
    )

    # Plotar distribuição normal sobreposta
    media_real = np.mean(amostras)
    desvio_padrao_real = np.std(amostras) / np.sqrt(tamanho_amostra)

    plotar_normal(medias_amostrais, media_real, desvio_padrao_real)

    axes[1].legend()

    plt.tight_layout()
    st.pyplot(fig)

# Executar o programa principal
if __name__ == "__main__":
    main()
