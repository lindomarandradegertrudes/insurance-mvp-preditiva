"""
estatistica.py
---------------
Estatísticas Populacionais e Visualização.

Gera métricas de distribuição e de média/agregação sobre a base sintética,
além dos gráficos (via Matplotlib) exibidos na aba "Exibir Estatísticas"
da interface:

  - Métricas de Distribuição:
      * Distribuição de Vínculos Empregatícios
      * Distribuição de Volume de Seguros por Cliente
  - Métricas de Média e Agregação:
      * Média de Idade e Renda
      * Média de Tempo de Permanência
      * Taxa Geral de Adimplência vs. Inadimplência
      * Score Médio da População

Nenhuma biblioteca de ML é usada — apenas 'statistics', 'math' e Matplotlib.
"""

import statistics
from collections import Counter

# Usamos a API orientada a objetos do Matplotlib (Figure) diretamente,
# em vez de pyplot, para evitar qualquer dependência de backend gráfico
# interativo aqui. Quem embute a figura no Tkinter (interface.py) usa
# FigureCanvasTkAgg com o objeto Figure retornado por plotar_estatisticas().
from matplotlib.figure import Figure


def calcular_metricas_agregacao(base_clientes):
    """
    Calcula manualmente (com o módulo 'statistics') as métricas de
    média e agregação exigidas pelo desafio.
    """
    idades = [c["idade"] for c in base_clientes]
    rendas = [c["renda_num"] for c in base_clientes]
    tempos_emprego = [c["tempo_emprego"] for c in base_clientes]
    scores = [c["score_geral"] for c in base_clientes]

    adimplentes = sum(1 for c in base_clientes if c["historico_credito"] in ("Bom", "Regular"))
    inadimplentes = len(base_clientes) - adimplentes

    return {
        "media_idade": round(statistics.mean(idades), 1),
        "media_renda": round(statistics.mean(rendas), 2),
        "media_tempo_emprego": round(statistics.mean(tempos_emprego), 1),
        "taxa_adimplencia_pct": round(100 * adimplentes / len(base_clientes), 1),
        "taxa_inadimplencia_pct": round(100 * inadimplentes / len(base_clientes), 1),
        "score_medio_populacao": round(statistics.mean(scores), 1),
    }


def calcular_distribuicoes(base_clientes):
    """Calcula as contagens de distribuição usadas nos histogramas/gráficos de barra."""
    vinculos = Counter(c["tipo_vinculo"] for c in base_clientes)
    volume_seguros = Counter(c["qtd_seguros_ativos"] for c in base_clientes)
    return {
        "distribuicao_vinculos": dict(sorted(vinculos.items())),
        "distribuicao_volume_seguros": dict(sorted(volume_seguros.items())),
    }


def gerar_relatorio_texto(base_clientes):
    """Monta um pequeno relatório textual (para exibir em um Label/Text da GUI)."""
    m = calcular_metricas_agregacao(base_clientes)
    linhas = [
        f"Total de clientes na base: {len(base_clientes)}",
        f"Média de Idade: {m['media_idade']} anos",
        f"Média de Renda: R$ {m['media_renda']:,.2f}",
        f"Média de Tempo de Emprego: {m['media_tempo_emprego']} anos",
        f"Taxa de Adimplência: {m['taxa_adimplencia_pct']}%",
        f"Taxa de Inadimplência: {m['taxa_inadimplencia_pct']}%",
        f"Score Médio da População: {m['score_medio_populacao']} / 100",
    ]
    return "\n".join(linhas)


def plotar_estatisticas(base_clientes):
    """
    Gera a figura Matplotlib com 2 gráficos lado a lado, prontos para
    serem embutidos em um FigureCanvasTkAgg na interface:

      1. Distribuição de Vínculos Empregatícios (barras)
      2. Distribuição de Volume de Seguros por Cliente (barras)

    Retorna o objeto `Figure` do Matplotlib (não chama plt.show() —
    quem decide como exibir é a camada de interface).
    """
    dist = calcular_distribuicoes(base_clientes)

    fig = Figure(figsize=(10, 4.5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # Gráfico 1: Distribuição de Vínculos Empregatícios
    vinculos = dist["distribuicao_vinculos"]
    ax1.bar(list(vinculos.keys()), list(vinculos.values()), color="#2E75B6")
    ax1.set_title("Distribuição de Vínculos Empregatícios")
    ax1.set_ylabel("Nº de clientes")
    ax1.tick_params(axis="x", rotation=30)

    # Gráfico 2: Distribuição de Volume de Seguros por Cliente
    volume = dist["distribuicao_volume_seguros"]
    ax2.bar([str(k) for k in volume.keys()], list(volume.values()), color="#1A7A5E")
    ax2.set_title("Volume de Seguros Ativos por Cliente")
    ax2.set_xlabel("Qtd. de seguros ativos")
    ax2.set_ylabel("Nº de clientes")

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    from gerador_base import gerar_base

    base = gerar_base(100, seed=42)
    print(gerar_relatorio_texto(base))
    print()
    print("Distribuições:", calcular_distribuicoes(base))

    fig = plotar_estatisticas(base)
    fig.savefig("/tmp/estatisticas_teste.png", dpi=100)
    print("\nGráfico de teste salvo em /tmp/estatisticas_teste.png")
