"""
gerador_base.py
----------------
Motor de Dados Sintéticos (Geração de Input).

Responsável por criar uma base de clientes fictícios para a seguradora,
seguindo relações de CAUSA -> EFEITO PROBABILÍSTICO coerentes com o
mercado de seguros (e não puramente aleatórias):

  1. Maior Renda        -> Aumenta chance de posse de imóvel e veículo
  2. Crédito Positivo    -> Aumenta tendência geral de contratação
  3. Volume de Seguros   -> Aumenta tempo estimado de permanência (reduz churn)
  4. Casado(a) + Filhos  -> Dispara a propensão ao Seguro de Vida

Nenhuma biblioteca de Machine Learning é utilizada aqui. Apenas
'random', 'math' e listas/dicionários puros de Python.
"""

import random
import math

# ----------------------------------------------------------------------
# Domínios (opções que aparecem nos campos selecionáveis da interface)
# ----------------------------------------------------------------------

FAIXAS_RENDA = [
    ("Até R$ 2.000", 1500),
    ("R$ 2.000 a R$ 5.000", 3500),
    ("R$ 5.000 a R$ 10.000", 7500),
    ("R$ 10.000 a R$ 20.000", 15000),
    ("Acima de R$ 20.000", 25000),
]

TIPOS_VINCULO = {
    "CLT": 0.75,
    "Servidor Público": 1.00,
    "Autônomo": 0.40,
    "Empresário": 0.60,
    "Aposentado": 0.70,
}

HISTORICOS_CREDITO = {
    "Bom": 1.0,
    "Regular": 0.5,
    "Ruim": 0.0,
}

ESTADOS_CIVIS = ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]

FAIXAS_ETARIAS_FILHOS = [
    "Não se aplica",
    "0-6 anos",
    "7-12 anos",
    "13-17 anos",
    "18+ anos",
]

SIM_NAO = ["Sim", "Não"]


def _sorteia_faixa_renda():
    """Sorteia uma faixa de renda com leve viés para a faixa intermediária."""
    pesos = [15, 30, 30, 18, 7]
    return random.choices(FAIXAS_RENDA, weights=pesos, k=1)[0]


def _probabilidade_por_renda(renda_num, base, ganho_max):
    """
    Converte renda numérica (R$) em uma probabilidade entre `base` e
    `base + ganho_max`, normalizando pela maior faixa de renda (25000).
    Usada para: posse de imóvel, posse de veículo, etc.
    """
    fator = min(renda_num / 25000, 1.0)
    return min(base + fator * ganho_max, 0.97)


def _sorteia_historico_credito(renda_num):
    """Crédito positivo é levemente mais provável em rendas maiores,
    mas mantém aleatoriedade real (não é determinístico)."""
    fator = min(renda_num / 25000, 1.0)
    pesos = {
        "Bom": 30 + fator * 35,
        "Regular": 45,
        "Ruim": 25 - fator * 15,
    }
    chaves = list(pesos.keys())
    valores = [max(pesos[k], 1) for k in chaves]
    return random.choices(chaves, weights=valores, k=1)[0]


def gerar_cliente(cliente_id):
    """Gera um único cliente sintético coerente."""
    idade = random.randint(18, 75)

    renda_label, renda_num = _sorteia_faixa_renda()

    tipo_vinculo = random.choice(list(TIPOS_VINCULO.keys()))

    # Tempo de emprego coerente com a idade (nunca maior que idade - 16)
    tempo_emprego_max = max(idade - 16, 0)
    tempo_emprego = random.randint(0, min(tempo_emprego_max, 40))

    # Causa 1: Maior Renda -> Aumento na chance de posse de imóvel e veículo
    prob_imovel = _probabilidade_por_renda(renda_num, base=0.10, ganho_max=0.75)
    prob_veiculo = _probabilidade_por_renda(renda_num, base=0.15, ganho_max=0.70)
    possui_imovel = "Sim" if random.random() < prob_imovel else "Não"
    possui_veiculo = "Sim" if random.random() < prob_veiculo else "Não"

    historico_credito = _sorteia_historico_credito(renda_num)

    estado_civil = random.choice(ESTADOS_CIVIS)
    casado = estado_civil == "Casado(a)"

    # Casados tendem a ter mais filhos
    if casado:
        qtd_filhos = random.choices([0, 1, 2, 3, 4], weights=[15, 30, 30, 18, 7], k=1)[0]
    else:
        qtd_filhos = random.choices([0, 1, 2, 3, 4], weights=[55, 25, 12, 6, 2], k=1)[0]

    if qtd_filhos == 0:
        faixa_etaria_filhos = "Não se aplica"
    else:
        faixa_etaria_filhos = random.choice(FAIXAS_ETARIAS_FILHOS[1:])

    # Causa 2: Crédito Positivo -> Maior tendência geral de contratação
    credito_score = HISTORICOS_CREDITO[historico_credito]
    prob_seguro = 0.20 + credito_score * 0.55 + min(renda_num / 25000, 1.0) * 0.15
    possui_seguro = "Sim" if random.random() < min(prob_seguro, 0.95) else "Não"

    # Causa 3: Volume de Seguros -> Maior tempo estimado de permanência
    if possui_seguro == "Sim":
        qtd_seguros_ativos = random.choices([1, 2, 3, 4], weights=[45, 30, 17, 8], k=1)[0]
    else:
        qtd_seguros_ativos = 0

    cliente = {
        "id": cliente_id,
        "idade": idade,
        "faixa_renda": renda_label,
        "renda_num": renda_num,
        "tipo_vinculo": tipo_vinculo,
        "tempo_emprego": tempo_emprego,
        "possui_imovel": possui_imovel,
        "possui_veiculo": possui_veiculo,
        "historico_credito": historico_credito,
        "estado_civil": estado_civil,
        "qtd_filhos": qtd_filhos,
        "faixa_etaria_filhos": faixa_etaria_filhos,
        "possui_seguro": possui_seguro,
        "qtd_seguros_ativos": qtd_seguros_ativos,
    }

    # Variáveis-alvo (rótulos sintéticos) usadas para TREINAR a regressão.
    # Elas simulam o "comportamento real" do mercado a partir das mesmas
    # relações de causa->efeito, sempre com ruído gaussiano para evitar
    # um ajuste artificialmente perfeito (mais realista para o MVP).
    cliente.update(_gerar_alvos(cliente))
    return cliente


def _gerar_alvos(c):
    """
    Gera os valores-alvo (variáveis dependentes) que a Regressão Linear
    Múltipla, em modelo.py, vai aprender a reproduzir a partir das
    features do cliente. Cada fórmula reflete uma relação de negócio
    descrita no desafio (Causa -> Efeito Probabilístico).
    """
    credito_score = HISTORICOS_CREDITO[c["historico_credito"]]
    vinculo_score = TIPOS_VINCULO[c["tipo_vinculo"]]
    casado = 1.0 if c["estado_civil"] == "Casado(a)" else 0.0
    imovel = 1.0 if c["possui_imovel"] == "Sim" else 0.0
    veiculo = 1.0 if c["possui_veiculo"] == "Sim" else 0.0

    ruido = lambda escala=4.0: random.gauss(0, escala)

    # Score Geral: combina renda, crédito, estabilidade e tempo de emprego
    score_geral = (
        20
        + (c["renda_num"] / 25000) * 30
        + credito_score * 25
        + vinculo_score * 15
        + min(c["tempo_emprego"], 20) * 0.5
        + ruido(5)
    )

    # Propensão Seguro de Vida: dispara com Casado(a) + Filhos (regra do desafio)
    prop_vida = (
        10
        + casado * 20
        + min(c["qtd_filhos"], 4) * 8
        + (c["renda_num"] / 25000) * 20
        + ruido(6)
    )

    # Propensão Seguro Automóvel: puxada por posse de veículo e renda
    prop_auto = 10 + veiculo * 45 + (c["renda_num"] / 25000) * 25 + ruido(6)

    # Propensão Seguro Residencial: puxada por posse de imóvel e renda
    prop_residencial = 10 + imovel * 45 + (c["renda_num"] / 25000) * 25 + ruido(6)

    # Propensão Previdência Privada: cresce com idade e renda
    prop_previdencia = 5 + (c["idade"] / 75) * 45 + (c["renda_num"] / 25000) * 30 + ruido(6)

    # Risco de Churn (probabilidade de cancelamento): reduz com mais
    # seguros ativos e crédito positivo (maior volume -> maior permanência)
    churn_prob = (
        65
        - c["qtd_seguros_ativos"] * 11
        - credito_score * 20
        - min(c["tempo_emprego"], 15) * 0.6
        + ruido(6)
    )

    # Score de Tempo de Permanência: cresce com volume de seguros e crédito
    tempo_permanencia_score = (
        15
        + c["qtd_seguros_ativos"] * 14
        + credito_score * 20
        + vinculo_score * 10
        + ruido(5)
    )

    return {
        "score_geral": round(min(max(score_geral, 0), 100), 2),
        "prop_vida": round(min(max(prop_vida, 0), 100), 2),
        "prop_auto": round(min(max(prop_auto, 0), 100), 2),
        "prop_residencial": round(min(max(prop_residencial, 0), 100), 2),
        "prop_previdencia": round(min(max(prop_previdencia, 0), 100), 2),
        "churn_prob": round(min(max(churn_prob, 0), 100), 2),
        "tempo_permanencia_score": round(min(max(tempo_permanencia_score, 0), 100), 2),
    }


def gerar_base(n=100, seed=None):
    """Gera uma base de `n` clientes sintéticos (padrão: 100, conforme o desafio)."""
    if seed is not None:
        random.seed(seed)
    return [gerar_cliente(i + 1) for i in range(n)]


if __name__ == "__main__":
    base = gerar_base(100, seed=42)
    print(f"Base sintética gerada com {len(base)} clientes.")
    print("Exemplo do primeiro cliente:")
    for k, v in base[0].items():
        print(f"  {k}: {v}")
