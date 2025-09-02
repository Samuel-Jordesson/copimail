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
import winreg



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
    ║                    INSTALADOR COPIEMAIL                      ║
    ║                                                              ║
    ║  Sistema de migração de emails - Instalação automática      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def download_file(url, local_path):
    """Baixa um arquivo da internet"""
    try:
        urllib.request.urlretrieve(url, local_path)
        return True
    except Exception as e:
        print(f"  ❌ Erro ao baixar: {e}")
        return False



def configure_windows_path(install_dir):
    """Configura automaticamente o PATH do Windows"""
    try:
        # Abrir a chave do registro do usuário atual
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            "Environment", 
                            0, 
                            winreg.KEY_READ | winreg.KEY_WRITE)
        
        # Obter o PATH atual
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path = ""
        
        # Verificar se o diretório já está no PATH
        if install_dir in current_path:
            winreg.CloseKey(key)
            return True
        
        # Adicionar o novo diretório ao PATH
        if current_path:
            new_path = current_path + ";" + install_dir
        else:
            new_path = install_dir
        
        # Atualizar o PATH no registro
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        
        # Notificar o Windows sobre a mudança usando setx
        try:
            subprocess.run(["setx", "PATH", new_path], 
                         capture_output=True, check=True)
        except Exception as e:
            # Se setx falhar, usar apenas o registro
            pass
        
        return True
        
    except Exception as e:
        return False

def create_global_command(script_path):
    """Cria comando global para executar o sistema"""
    system = platform.system().lower()
    
    if system == "windows":
        # Windows - criar arquivo .bat
        batch_content = f'@echo off\npython "{script_path}" %*'
        batch_path = os.path.join(os.path.dirname(script_path), "copimail.bat")
        
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        # Configurar PATH automaticamente
        configure_windows_path(os.path.dirname(batch_path))
        
    else:
        # Linux/Mac - criar script executável
        shell_content = f'#!/bin/bash\npython3 "{script_path}" "$@"'
        shell_path = os.path.join(os.path.dirname(script_path), "copimail")
        
        with open(shell_path, 'w') as f:
            f.write(shell_content)
        
        os.chmod(shell_path, 0o755)

def download_system():
    """Baixa e instala o sistema completo"""
    # Criar diretório de instalação
    install_dir = os.path.expanduser("~/copimail")
    os.makedirs(install_dir, exist_ok=True)
    
    # Lista de arquivos para baixar
    files_to_download = {
        "copimail.py": f"{BASE_URL}/copimail.py",
        "requirements.txt": f"{BASE_URL}/requirements.txt",
        "version.json": f"{BASE_URL}/version.json"
    }
    
    # Barra de progresso unificada para toda a instalação
    print("Instalação em andamento...")
    
    # Definir etapas totais da instalação
    total_steps = len(files_to_download) + 3 + 3  # arquivos + dependências + configuração
    current_step = 0
    bar_length = 50
    
    # Mostrar barra inicial
    bar = '░' * bar_length
    print(f"\r  [{bar}] 0% - Iniciando...", end='', flush=True)
    
    # Download de arquivos
    for filename, url in files_to_download.items():
        current_step += 1
        progress = (current_step / total_steps) * 100
        filled_length = int(bar_length * current_step // total_steps)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Mostrar barra de progresso unificada
        print(f"\r  [{bar}] {progress:.0f}% - Baixando {filename}...", end='', flush=True)
        
        local_path = os.path.join(install_dir, filename)
        if not download_file(url, local_path):
            print(f"\nFalha na instalação: não foi possível baixar {filename}")
            return False
        
        # Pausa para visualizar o progresso
        import time
        time.sleep(0.2)
    
    # Instalar dependências
    dependencies = ["colorama", "pwinput", "tqdm"]
    for dep in dependencies:
        current_step += 1
        progress = (current_step / total_steps) * 100
        filled_length = int(bar_length * current_step // total_steps)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Mostrar barra de progresso unificada
        print(f"\r  [{bar}] {progress:.0f}% - Instalando {dep}...", end='', flush=True)
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            pass
        
        # Pausa para visualizar o progresso
        import time
        time.sleep(0.3)
    
    # Configuração do sistema
    config_steps = ["Criando comandos", "Configurando PATH", "Finalizando"]
    for step in config_steps:
        current_step += 1
        progress = (current_step / total_steps) * 100
        filled_length = int(bar_length * current_step // total_steps)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Mostrar barra de progresso unificada
        print(f"\r  [{bar}] {progress:.0f}% - {step}...", end='', flush=True)
        
        # Executar etapa
        if step == "Criando comandos":
            script_path = os.path.join(install_dir, "copimail.py")
            create_global_command(script_path)
        elif step == "Configurando PATH":
            # PATH já é configurado na função create_global_command
            pass
        
        # Pausa para visualizar o progresso
        import time
        time.sleep(0.3)
    
    # Completar a barra unificada
    print(f"\r  [{'█' * bar_length}] 100% - Instalação concluída!     ")
    
    print("\n" + "="*50)
    print("Pronto! CopiMail instalado com sucesso!")
    print("="*50)
    print("Agora só reiniciar o terminal e executar: copimail")
    print("="*50)
    
    return True

def main():
    """Função principal"""
    print_banner()
    
    # Verificar se Python está instalado
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return
    
    print(f"Python {sys.version.split()[0]} detectado")
    
    # Confirmar instalação
    print(f"\nSistema será baixado de: {BASE_URL}")
    confirm = input("Continuar com a instalação? (s/n): ").lower()
    
    if confirm != 's':
        print("Instalação cancelada.")
        return
    
    print("\nIniciando instalação...")
    
    # Executar instalação com barra de progresso unificada
    if download_system():
        print("\nCopiMail está pronto para uso!")
    else:
        print("\nFalha na instalação. Verifique a conexão com a internet.")
        return

if __name__ == "__main__":
    main()
