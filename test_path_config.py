#!/usr/bin/env python3
"""
Script de teste para verificar a configuração automática do PATH
"""

import os
import sys
import platform

def test_path_configuration():
    """Testa se o CopiMail está no PATH"""
    print("🧪 Testando configuração do PATH...")
    
    if platform.system().lower() == "windows":
        # Verificar se o comando copimail está disponível
        try:
            result = os.system("copimail --help >nul 2>&1")
            if result == 0:
                print("✅ Comando 'copimail' encontrado no PATH!")
                print("🎉 Configuração automática funcionou perfeitamente!")
                return True
            else:
                print("❌ Comando 'copimail' não encontrado no PATH")
                print("💡 Tente reiniciar o terminal/PowerShell")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar comando: {e}")
            return False
    else:
        print("ℹ️ Este teste é específico para Windows")
        return True

def show_path_info():
    """Mostra informações sobre o PATH atual"""
    print("\n📋 Informações do PATH:")
    print(f"🔍 Sistema: {platform.system()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    if platform.system().lower() == "windows":
        path = os.environ.get('PATH', '')
        print(f"📁 PATH atual: {path}")
        
        # Verificar se o diretório do CopiMail está no PATH
        copimail_dir = os.path.expanduser("~/copimail")
        if copimail_dir in path:
            print(f"✅ Diretório CopiMail encontrado no PATH: {copimail_dir}")
        else:
            print(f"❌ Diretório CopiMail NÃO encontrado no PATH: {copimail_dir}")

if __name__ == "__main__":
    print("🚀 TESTE DE CONFIGURAÇÃO DO COPIEMAIL")
    print("=" * 50)
    
    show_path_info()
    print("\n" + "=" * 50)
    
    if test_path_configuration():
        print("\n🎯 RESULTADO: Configuração funcionando!")
    else:
        print("\n⚠️ RESULTADO: Configuração precisa de ajustes")
        print("💡 Execute o instalador novamente ou reinicie o terminal")
    
    print("\n" + "=" * 50)
