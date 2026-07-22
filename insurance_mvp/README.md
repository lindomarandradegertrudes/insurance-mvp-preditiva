# MVP de Análise Preditiva para Seguros

Aplicação desktop em Python (Tkinter) que demonstra, na prática, Estatística,
Álgebra Linear e Regressão Linear Múltipla **implementada manualmente**
(sem scikit-learn / TensorFlow / Keras / PyTorch / XGBoost / LightGBM /
CatBoost), aplicada a um cenário de seguros.

## Como executar (Windows — PowerShell ou Git Bash)

1. Extraia o `.zip` em uma pasta, ex.: `C:\projetos\insurance_mvp`
2. Abra o terminal nessa pasta
3. Rode:

   ```bash
   python main.py
   ```

O `main.py` faz o **setup automático**: verifica se `numpy`, `pandas` e
`matplotlib` estão instalados e, se não estiverem, instala sozinho via
`pip` antes de abrir a interface gráfica.

> Requisito: Python 3.9+ com Tkinter habilitado (padrão no instalador
> oficial do [python.org](https://python.org) para Windows — marque a
> opção "tcl/tk and IDLE" se você customizou a instalação).

## Fluxo de uso na interface

1. **Gerar Base Sintética** → cria 100 clientes fictícios coerentes
   (relações causa→efeito, não aleatoriedade pura).
2. **Treinar Modelo** → treina 7 regressões lineares múltiplas manuais
   (Equação Normal com NumPy) sobre a base gerada e mostra o R² de cada uma.
3. Preencha o **Formulário de Cliente** (idade + campos selecionáveis) com
   o perfil que você quer analisar.
4. **Analisar Cliente** → aplica os modelos treinados e mostra o Painel de
   Predições Individuais (Score Geral, tendência de adimplência,
   propensão de contratação por produto, risco de churn e tempo estimado
   de permanência).
5. **Exibir Estatísticas** → mostra os gráficos populacionais (distribuição
   de vínculos empregatícios e de volume de seguros) e o relatório de
   médias/agregações.
6. **Limpar Dados** → reinicia a base e o modelo.

## Arquitetura (conforme especificação do desafio)

```
main.py            -> Orquestrador: setup automático + inicialização da GUI
interface.py        -> GUI Tkinter (formulário, botões, abas de resultado)
modelo.py            -> Regressão Linear Múltipla manual (Equação Normal) +
                        orquestração dos 7 modelos + codificação de features
gerador_base.py       -> Motor de dados sintéticos (100 clientes) + geração
                        dos alvos de treino (score, propensões, churn etc.)
estatistica.py         -> Estatísticas populacionais e gráficos Matplotlib
```

## Sobre a "Regra de Ouro" (regressão 100% manual)

Toda a matemática de `modelo.py` é escrita à mão com NumPy puro:

- **Normalização**: padronização z-score (`(x - média) / desvio`) calculada
  manualmente.
- **Cálculo de coeficientes**: Equação Normal `β = (XᵀX)⁻¹ · Xᵀ · y`,
  resolvida com `np.linalg.pinv` (pseudo-inversa, mais estável
  numericamente que `inv()` — ainda assim é álgebra linear pura, não uma
  função de ML pronta).
- **Predição**: aplicação direta da fórmula linear `ŷ = X · β`.

7 modelos independentes são treinados (um por variável de negócio):
`score_geral`, `prop_vida`, `prop_auto`, `prop_residencial`,
`prop_previdencia`, `churn_prob`, `tempo_permanencia_score`.

## Testando os módulos isoladamente

Cada módulo tem um bloco `if __name__ == "__main__":` para teste isolado:

```bash
python gerador_base.py   # gera e imprime um cliente de exemplo
python modelo.py         # testa a regressão manual com dados sintéticos
python estatistica.py    # calcula estatísticas e salva um gráfico de teste
```

## Checklist de entrega (páginas 199 da apostila)

- [x] Arquitetura modular (`main`, `interface`, `modelo`, `gerador_base`, `estatistica`)
- [x] Regressão Linear Múltipla implementada manualmente (Equação Normal)
- [x] Interface gráfica Tkinter usável, com formulário e painel de ações
- [x] Gráficos e estatísticas populacionais claros (Matplotlib)
- [x] Código comentado e documentado
- [x] Setup automático com tratamento de erros de instalação
