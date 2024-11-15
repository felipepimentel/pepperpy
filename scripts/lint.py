#!/usr/bin/env python  # noqa: EXE001
"""Verificador de Lint para o projeto PepperPy."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def is_tool_available(tool: str) -> bool:
    """Verifica se uma ferramenta está disponível no PATH do sistema."""
    return shutil.which(tool) is not None


def run_command(cmd: list[str]) -> bool:
    """Executa um comando e exibe a saída detalhada para arquivos problemáticos.

    Args:
        cmd (list[str]): Comando a ser executado.

    Returns:
        bool: True se o comando for bem-sucedido, False caso contrário.
    """
    print(f"\nExecutando: {' '.join(cmd)}")
    try:
        # Executa o comando e captura a saída
        subprocess.run(
            cmd,
            check=True,
            cwd=ROOT_DIR,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"{cmd[0]} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        # Imprime a saída detalhada do linter
        print(f"{cmd[0]} encontrou problemas. Detalhes abaixo:\n")
        print(e.stdout or e.stderr)

        # Coleta e imprime um resumo dos arquivos problemáticos
        problematic_files = set()
        output = e.stdout.strip().splitlines() + e.stderr.strip().splitlines()
        for line in output:
            # Trata a saída do Ruff
            if ":" in line:
                parts = line.split(":")
                filename = parts[0].strip()
                if (ROOT_DIR / filename).exists():
                    problematic_files.add(filename)

        if problematic_files:
            print("\nResumo dos arquivos problemáticos:")
            for filename in sorted(problematic_files):
                print(f"- {filename}")

        return False


def run_linters() -> bool:
    """Executa todos os linters com modo de correção automática.

    Returns:
        bool: True se todos os linters forem bem-sucedidos, False caso contrário.
    """
    print("Executando linters...")

    # Verifica se as ferramentas necessárias estão instaladas
    required_tools = ["ruff"]
    missing_tools = [tool for tool in required_tools if not is_tool_available(tool)]
    if missing_tools:
        print(
            f"Ferramentas ausentes: {', '.join(missing_tools)}. Por favor, instale-as e tente novamente.",
        )
        return False

    # Lista de comandos dos linters a serem executados
    linters = [
        ["ruff", "check", "--fix", "."],
    ]

    success = True
    for cmd in linters:
        if not run_command(cmd):
            success = False

    if not success:
        print("\nAlguns linters falharam. Por favor, corrija os problemas acima.")
    else:
        print("\nTodos os linters foram executados com sucesso!")

    return success


if __name__ == "__main__":
    sys.exit(0 if run_linters() else 1)
