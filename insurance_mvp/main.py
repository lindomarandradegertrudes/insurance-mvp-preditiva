"""
main.py
-------
Orquestrador do MVP de Análise Preditiva para Seguros.

Setup Automático (conforme especificação):
  Passo 1: Verificar bibliotecas exigidas.
  Passo 2: Instalar ausentes automaticamente via pip.
  Passo 3: Reportar eventuais erros de instalação.
  Passo 4: Liberar execução da aplicação (GUI).

Execução: no Windows (PowerShell ou Git Bash), a partir da pasta do projeto:
    python main.py
"""

import sys
import subprocess
import importlib

# Bibliotecas de terceiros exigidas pelo projeto (as demais — os, sys,
# subprocess, importlib, math, statistics, random, csv, json, tkinter —
# já fazem parte da biblioteca padrão do Python e não precisam de pip).
BIBLIOTECAS_EXIGIDAS = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
}


def passo1_verificar_bibliotecas():
    """Passo 1: Verifica quais bibliotecas exigidas já estão instaladas."""
    faltando = []
    for modulo, pacote_pip in BIBLIOTECAS_EXIGIDAS.items():
        try:
            importlib.import_module(modulo)
        except ImportError:
            faltando.append(pacote_pip)
    return faltando


def passo2_instalar_ausentes(pacotes_faltando):
    """Passo 2: Instala automaticamente, via pip, as bibliotecas ausentes."""
    erros = []
    for pacote in pacotes_faltando:
        print(f"[Setup] Instalando '{pacote}' via pip...")
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "install", pacote],
            capture_output=True,
            text=True,
        )
        if resultado.returncode != 0:
            erros.append((pacote, resultado.stderr.strip()))
        else:
            print(f"[Setup] '{pacote}' instalado com sucesso.")
    return erros


def passo3_reportar_erros(erros):
    """Passo 3: Reporta eventuais erros de instalação e interrompe se necessário."""
    if not erros:
        return True
    print("\n[Setup] ERRO: não foi possível instalar as seguintes bibliotecas:")
    for pacote, msg in erros:
        print(f"  - {pacote}: {msg}")
    print(
        "\nInstale manualmente com:\n"
        f"    {sys.executable} -m pip install " + " ".join(p for p, _ in erros)
    )
    return False


def passo4_liberar_execucao():
    """Passo 4: Libera a execução da aplicação (GUI Tkinter)."""
    try:
        import tkinter  # noqa: F401
    except ImportError:
        print(
            "\n[Setup] ERRO: o módulo 'tkinter' não está disponível nesta instalação "
            "do Python.\nNo Windows, reinstale o Python marcando a opção 'tcl/tk and "
            "IDLE' no instalador oficial (python.org)."
        )
        sys.exit(1)

    from interface import iniciar_aplicacao
    print("[Setup] Ambiente OK. Iniciando a interface gráfica...\n")
    iniciar_aplicacao()


def main():
    print("=" * 60)
    print(" MVP de Análise Preditiva para Seguros — Setup Automático")
    print("=" * 60)

    faltando = passo1_verificar_bibliotecas()

    if faltando:
        print(f"[Setup] Bibliotecas ausentes detectadas: {', '.join(faltando)}")
        erros = passo2_instalar_ausentes(faltando)
        if not passo3_reportar_erros(erros):
            sys.exit(1)
    else:
        print("[Setup] Todas as bibliotecas exigidas já estão instaladas.")

    passo4_liberar_execucao()


if __name__ == "__main__":
    main()
