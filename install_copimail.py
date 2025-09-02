#!/usr/bin/env python3
"""
Script de instalação do CopiMail
Baixa o sistema do GitHub e instala como comando global
"""

import os
import sys
import urllib.request
import subprocess
import json
import platform

# CONFIGURAÇÃO DO REPOSITÓRIO
GITHUB_USER = "Samuel-Jordesson"  # SEU USUARIO GITHUB
GITHUB_REPO = "copimail"
GITHUB_BRANCH = "main"

# URLs de download
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"

def print_banner():
    """Exibe banner do instalador"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 INSTALADOR COPIEMAIL 🚀                ║
    ║                                                              ║
    ║  Sistema de migração de emails - Instalação automática      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def download_file(url, local_path):
    """Baixa um arquivo da internet"""
    try:
        print(f"  📥 Baixando: {os.path.basename(local_path)}")
        urllib.request.urlretrieve(url, local_path)
        print(f"  ✅ Baixado com sucesso!")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao baixar: {e}")
        return False

def install_dependencies():
    """Instala as dependências necessárias"""
    print("\n📦 Instalando dependências...")
    
    dependencies = [
        "colorama",
        "pwinput", 
        "tqdm"
    ]
    
    for dep in dependencies:
        try:
            print(f"  📦 Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         capture_output=True, check=True)
            print(f"  ✅ {dep} instalado!")
        except subprocess.CalledProcessError:
            print(f"  ❌ Erro ao instalar {dep}")

def create_global_command(script_path):
    """Cria comando global para executar o sistema"""
    print("\n🔧 Criando comando global...")
    
    system = platform.system().lower()
    
    if system == "windows":
        # Windows - criar arquivo .bat
        batch_content = f'@echo off\npython "{script_path}" %*'
        batch_path = os.path.join(os.path.dirname(script_path), "copimail.bat")
        
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"  ✅ Comando criado: {batch_path}")
        print("  💡 Adicione o diretório ao PATH do Windows:")
        print(f"     {os.path.dirname(batch_path)}")
        
    else:
        # Linux/Mac - criar script executável
        shell_content = f'#!/bin/bash\npython3 "{script_path}" "$@"'
        shell_path = os.path.join(os.path.dirname(script_path), "copimail")
        
        with open(shell_path, 'w') as f:
            f.write(shell_content)
        
        os.chmod(shell_path, 0o755)
        
        print(f"  ✅ Comando criado: {shell_path}")
        print("  💡 Adicione ao PATH:")
        print(f"     export PATH=\"$PATH:{os.path.dirname(shell_path)}\"")

def download_system():
    """Baixa e instala o sistema completo"""
    print("🚀 Iniciando instalação do CopiMail...")
    
    # Criar diretório de instalação
    install_dir = os.path.expanduser("~/copimail")
    os.makedirs(install_dir, exist_ok=True)
    
    print(f"📁 Diretório de instalação: {install_dir}")
    
    # Lista de arquivos para baixar
    files_to_download = {
        "copimail.py": f"{BASE_URL}/copimail.py",
        "requirements.txt": f"{BASE_URL}/requirements.txt",
        "version.json": f"{BASE_URL}/version.json"
    }
    
    # Baixar arquivos
    print("\n📥 Baixando arquivos do sistema...")
    for filename, url in files_to_download.items():
        local_path = os.path.join(install_dir, filename)
        if not download_file(url, local_path):
            print(f"❌ Falha na instalação: não foi possível baixar {filename}")
            return False
    
    # Instalar dependências
    install_dependencies()
    
    # Criar comando global
    script_path = os.path.join(install_dir, "copimail.py")
    create_global_command(script_path)
    
    print("\n" + "="*60)
    print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print(f"📁 Sistema instalado em: {install_dir}")
    print("💡 Para usar o sistema:")
    
    if platform.system().lower() == "windows":
        print("   1. Adicione o diretório ao PATH do Windows")
        print("   2. Execute: copimail")
    else:
        print("   1. Adicione ao PATH: export PATH=\"$PATH:{install_dir}\"")
        print("   2. Execute: copimail")
    
    print("\n🔄 Para atualizar: execute este script novamente")
    print("="*60)
    
    return True

def main():
    """Função principal"""
    print_banner()
    
    # Verificar se Python está instalado
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    
    # Confirmar instalação
    print(f"\n📋 Sistema será baixado de: {BASE_URL}")
    confirm = input("🤔 Continuar com a instalação? (s/n): ").lower()
    
    if confirm != 's':
        print("❌ Instalação cancelada.")
        return
    
    # Executar instalação
    if download_system():
        print("\n🎯 CopiMail está pronto para uso!")
    else:
        print("\n💥 Falha na instalação. Verifique a conexão com a internet.")

if __name__ == "__main__":
    main()
