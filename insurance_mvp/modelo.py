"""
modelo.py
---------
O Core Matemático (Regressão Linear Múltipla) — Implementação 100% manual.
Zero modelos prontos (sem scikit-learn, sem statsmodels).

Etapas implementadas manualmente, conforme a especificação:
  1. Álgebra Linear   -> manipulação de matrizes e vetores com NumPy
  2. Normalização      -> padronização (z-score) escrita à mão
  3. Cálculo de Coef.  -> Equação Normal:  beta = (XtX)^-1 . Xt . y
  4. Motor de Predição -> aplicação da fórmula linear: y = X . beta
"""

import numpy as np


class RegressaoLinearMultipla:
    """
    Regressão Linear Múltipla implementada manualmente via Equação Normal.

        y = b0 + b1*x1 + b2*x2 + ... + bn*xn

    A normalização (z-score) é calculada e armazenada internamente para
    que novos clientes possam ser escorados de forma consistente com os
    dados de treino.
    """

    def __init__(self, nome_variavel="alvo"):
        self.nome_variavel = nome_variavel
        self.medias = None
        self.desvios = None
        self.coeficientes = None  # beta, incluindo o intercepto (b0)
        self.treinado = False

    # ------------------------------------------------------------------
    # 2. Normalização (Padronização Z-score) — escrita manualmente
    # ------------------------------------------------------------------
    def _normalizar(self, X, ajustar=False):
        """
        Padroniza cada coluna de X: z = (x - media) / desvio_padrao.
        Se ajustar=True, calcula e guarda média/desvio (etapa de treino).
        Caso contrário, reaplica média/desvio já guardados (predição).
        """
        X = np.array(X, dtype=float)

        if ajustar:
            self.medias = X.mean(axis=0)
            desvios = X.std(axis=0)
            # Evita divisão por zero em colunas constantes
            desvios[desvios == 0] = 1.0
            self.desvios = desvios

        return (X - self.medias) / self.desvios

    # ------------------------------------------------------------------
    # 3. Cálculo de Coeficientes — Equação Normal (Álgebra Linear manual)
    # ------------------------------------------------------------------
    def treinar(self, X, y):
        """
        Treina o modelo a partir da matriz de features X (n_amostras x n_features)
        e do vetor alvo y (n_amostras,).

        Resolve manualmente:  beta = (Xt . X)^-1 . Xt . y
        Usando pseudo-inversa (np.linalg.pinv) para estabilidade numérica
        (equivalente matemático, sem chamar nenhum ".fit()" de biblioteca de ML).
        """
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float).reshape(-1, 1)

        # Etapa 1: Normalização das features
        Xn = self._normalizar(X, ajustar=True)

        # Etapa 2: Adiciona a coluna de bias (intercepto) -> X = [1, x1, x2, ...]
        n_amostras = Xn.shape[0]
        bias = np.ones((n_amostras, 1))
        Xb = np.hstack([bias, Xn])  # Álgebra Linear: concatenação de matrizes

        # Etapa 3: Equação Normal -> beta = (Xt.X)^-1 . Xt.y
        Xt = Xb.T
        XtX = Xt @ Xb
        XtX_inv = np.linalg.pinv(XtX)  # pseudo-inversa (mais estável que inv())
        Xty = Xt @ y

        self.coeficientes = XtX_inv @ Xty  # vetor beta (n_features+1, 1)
        self.treinado = True
        return self

    # ------------------------------------------------------------------
    # 4. Motor de Predição — aplicação manual da fórmula linear
    # ------------------------------------------------------------------
    def prever(self, X):
        """
        Aplica a fórmula linear treinada a novas amostras:
            y_pred = b0 + b1*x1n + b2*x2n + ... + bn*xnn
        """
        if not self.treinado:
            raise RuntimeError(
                f"O modelo '{self.nome_variavel}' ainda não foi treinado. "
                "Clique em 'Treinar Modelo' antes de 'Analisar Cliente'."
            )

        X = np.array(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(1, -1)

        Xn = self._normalizar(X, ajustar=False)
        n_amostras = Xn.shape[0]
        bias = np.ones((n_amostras, 1))
        Xb = np.hstack([bias, Xn])

        y_pred = Xb @ self.coeficientes
        return y_pred.flatten()

    def r2_score(self, X, y):
        """Calcula manualmente o coeficiente de determinação R^2 (qualidade do ajuste)."""
        y = np.array(y, dtype=float).flatten()
        y_pred = self.prever(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y.mean()) ** 2)
        if ss_tot == 0:
            return 1.0
        return 1 - (ss_res / ss_tot)


def clip(valor, minimo=0.0, maximo=100.0):
    """Restringe um valor previsto ao intervalo de negócio válido (ex.: 0-100%)."""
    return max(minimo, min(maximo, valor))


def bucket_tempo_permanencia(score_0_100):
    """
    Converte o score contínuo de permanência (0-100) prevista pela regressão
    em uma das faixas de negócio definidas no desafio:
    <6 meses, 6m-1ano, 1-2 anos, 2-5 anos, 5-10 anos, >10 anos.
    """
    if score_0_100 < 20:
        return "< 6 meses"
    elif score_0_100 < 40:
        return "6 meses - 1 ano"
    elif score_0_100 < 60:
        return "1 - 2 anos"
    elif score_0_100 < 80:
        return "2 - 5 anos"
    elif score_0_100 < 92:
        return "5 - 10 anos"
    else:
        return "> 10 anos"


class ModeloPreditivoSeguros:
    """
    Orquestra 7 regressões lineares múltiplas independentes (uma para cada
    variável de negócio) treinadas sobre a mesma base sintética de clientes.
    Gera o "Painel de Predições Individuais" para um cliente qualquer.
    """

    # Nome das colunas de feature, na ordem em que entram na matriz X
    COLUNAS_FEATURES = [
        "idade",
        "renda_num",
        "vinculo_score",
        "tempo_emprego",
        "imovel_bin",
        "veiculo_bin",
        "credito_score",
        "casado_bin",
        "qtd_filhos",
        "seguro_bin",
        "qtd_seguros_ativos",
    ]

    ALVOS = [
        "score_geral",
        "prop_vida",
        "prop_auto",
        "prop_residencial",
        "prop_previdencia",
        "churn_prob",
        "tempo_permanencia_score",
    ]

    def __init__(self):
        self.modelos = {alvo: RegressaoLinearMultipla(alvo) for alvo in self.ALVOS}
        self.r2 = {}
        self.treinado = False

    @staticmethod
    def codificar_features(cliente):
        """
        Converte um dicionário de cliente (vindo do gerador_base.py OU
        preenchido manualmente na interface Tkinter) em um vetor numérico
        na ordem definida por COLUNAS_FEATURES. É a MESMA função usada no
        treino e na predição, garantindo consistência.
        """
        # Importa os dicionários de mapeamento do gerador_base para evitar duplicação
        from gerador_base import TIPOS_VINCULO, HISTORICOS_CREDITO

        vinculo_score = TIPOS_VINCULO.get(cliente["tipo_vinculo"], 0.5)
        credito_score = HISTORICOS_CREDITO.get(cliente["historico_credito"], 0.5)
        imovel_bin = 1.0 if cliente["possui_imovel"] == "Sim" else 0.0
        veiculo_bin = 1.0 if cliente["possui_veiculo"] == "Sim" else 0.0
        casado_bin = 1.0 if cliente["estado_civil"] == "Casado(a)" else 0.0
        seguro_bin = 1.0 if cliente["possui_seguro"] == "Sim" else 0.0

        return [
            float(cliente["idade"]),
            float(cliente["renda_num"]),
            vinculo_score,
            float(cliente["tempo_emprego"]),
            imovel_bin,
            veiculo_bin,
            credito_score,
            casado_bin,
            float(cliente["qtd_filhos"]),
            seguro_bin,
            float(cliente["qtd_seguros_ativos"]),
        ]

    def treinar(self, base_clientes):
        """
        Treina os 7 modelos a partir de uma lista de dicionários de clientes
        (gerada por gerador_base.gerar_base), cada um já contendo os alvos
        sintéticos (score_geral, prop_vida, etc.).
        """
        if not base_clientes:
            raise ValueError("A base de clientes está vazia. Gere a base sintética primeiro.")

        X = [self.codificar_features(c) for c in base_clientes]

        for alvo in self.ALVOS:
            y = [c[alvo] for c in base_clientes]
            self.modelos[alvo].treinar(X, y)
            self.r2[alvo] = self.modelos[alvo].r2_score(X, y)

        self.treinado = True
        return self.r2

    def analisar_cliente(self, cliente):
        """
        Aplica os 7 modelos treinados a um único cliente (novo, vindo do
        formulário da GUI) e monta o Painel de Predições Individuais
        exatamente como especificado no desafio:

          - Indicadores Globais: Score Geral, Tendência Adimplência/Inadimplência
          - Propensão de Contratação (%): Vida, Automóvel, Residencial, Previdência
          - Risco e Retenção (Churn): Probabilidade de Cancelamento + Tempo Estimado
        """
        if not self.treinado:
            raise RuntimeError("Treine o modelo antes de analisar um cliente.")

        x = self.codificar_features(cliente)

        score_geral = clip(self.modelos["score_geral"].prever(x)[0])
        prop_vida = clip(self.modelos["prop_vida"].prever(x)[0])
        prop_auto = clip(self.modelos["prop_auto"].prever(x)[0])
        prop_residencial = clip(self.modelos["prop_residencial"].prever(x)[0])
        prop_previdencia = clip(self.modelos["prop_previdencia"].prever(x)[0])
        churn_prob = clip(self.modelos["churn_prob"].prever(x)[0])
        tempo_score = clip(self.modelos["tempo_permanencia_score"].prever(x)[0])

        tendencia = "Adimplência" if score_geral >= 50 else "Inadimplência"

        return {
            "indicadores_globais": {
                "score_geral": round(score_geral, 1),
                "tendencia": tendencia,
            },
            "propensao_contratacao": {
                "Seguro de Vida": round(prop_vida, 1),
                "Seguro Automóvel": round(prop_auto, 1),
                "Seguro Residencial": round(prop_residencial, 1),
                "Previdência Privada": round(prop_previdencia, 1),
            },
            "risco_retencao": {
                "probabilidade_churn": round(churn_prob, 1),
                "tempo_estimado_permanencia": bucket_tempo_permanencia(tempo_score),
            },
        }


if __name__ == "__main__":
    # Teste rápido e isolado do motor matemático com dados sintéticos simples
    rng = np.random.default_rng(0)
    X_teste = rng.normal(size=(200, 3))
    y_teste = 10 + 2 * X_teste[:, 0] - 3 * X_teste[:, 1] + 0.5 * X_teste[:, 2] + rng.normal(scale=0.1, size=200)

    modelo = RegressaoLinearMultipla("teste")
    modelo.treinar(X_teste, y_teste)
    print("Coeficientes (b0, b1, b2, b3):", modelo.coeficientes.flatten())
    print("R^2:", modelo.r2_score(X_teste, y_teste))
