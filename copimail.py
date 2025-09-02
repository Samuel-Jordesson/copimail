import imaplib
import email
import getpass
from colorama import init, Fore, Style
import pwinput
from tqdm import tqdm
import time

IMAP_SERVER = "imap.hostinger.com"
PORT = 993


def connect_imap(email_user, password):
    """Conecta na conta IMAP"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, PORT)
        mail.login(email_user, password)
        return mail
    except Exception as e:
        print(Fore.RED + f"\n❌ Erro ao conectar: {str(e)}" + Style.RESET_ALL)
        return None


def migrate_inbox(old_email, old_password, new_email, new_password):
    old_mail = connect_imap(old_email, old_password)
    new_mail = connect_imap(new_email, new_password)

    try:
        # Seleciona a INBOX da conta antiga
        status, _ = old_mail.select("INBOX")
        if status != "OK":
            print("❌ Não consegui acessar a INBOX da conta antiga.")
            return

        # Busca todos os emails
        status, data = old_mail.search(None, "ALL")
        email_ids = data[0].split()
        total_emails = len(email_ids)
        print(f"\n📨 {total_emails} e-mails encontrados para migrar.\n")
        input("Pressione Enter para começar a migração...")

        # Cria barra de progresso
        with tqdm(total=total_emails, desc="📤 Migrando emails", 
                  bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                  colour='green') as pbar:
            
            # Migra os emails
            for i, e_id in enumerate(email_ids, 1):
                try:
                    _, msg_data = old_mail.fetch(e_id, "(RFC822)")
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    # Mantém a data original
                    date_tuple = email.utils.parsedate(msg["Date"])
                    internal_date = imaplib.Time2Internaldate(date_tuple) if date_tuple else None

                    # Adiciona na nova conta
                    new_mail.append("INBOX", "", internal_date, raw_email)

                    # Atualiza a barra de progresso
                    pbar.set_postfix_str(f"Email {i}/{total_emails}")
                    pbar.update(1)
                    
                    # Pequena pausa para não sobrecarregar o servidor
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"\n⚠️ Erro ao migrar email {i}: {str(e)}")
                    pbar.update(1)
                    continue

        print(f"\n\n✅ Migração concluída com sucesso! {total_emails} e-mails migrados.")

    finally:
        old_mail.close()
        old_mail.logout()
        new_mail.logout()


def migrate_bulk(migration_list):
    """Executa migrações em massa"""
    total_migrations = len(migration_list)
    print(f"\n🚀 Iniciando {total_migrations} migrações em massa...\n")
    
    # Barra de progresso para as migrações
    with tqdm(total=total_migrations, desc="🔄 Executando migrações", 
              bar_format='{l_bar}{bar}| {n_fmt}/{total_migrations} [{elapsed}<{remaining}, {rate_fmt}]',
              colour='blue') as pbar:
        
        for i, (old_email, old_password, new_email, new_password) in enumerate(migration_list, 1):
            try:
                print(f"\n📧 Migração {i}/{total_migrations}: {old_email} → {new_email}")
                migrate_inbox(old_email, old_password, new_email, new_password)
                pbar.update(1)
                
            except Exception as e:
                print(f"\n❌ Erro na migração {i}: {str(e)}")
                pbar.update(1)
                continue
    
    print(f"\n🎉 Todas as {total_migrations} migrações foram concluídas!")


def individual_migration():
    """Executa uma migração individual"""
    print(Fore.LIGHTCYAN_EX + "🔄 MIGRAÇÃO INDIVIDUAL" + Style.RESET_ALL)
    
    # Loop para garantir dados corretos
    while True:
        # Solicita email e senha da conta antiga
        old_email = input_azul("Digite o email que deseja migrar: ")
        old_password = pwinput.pwinput("Digite a senha deste email: ", mask='*')

        # Solicita email e senha da conta nova
        new_email = input_azul("Digite o email para onde deseja enviar: ")
        new_password = pwinput.pwinput("Digite a senha deste email: ", mask='*')

        # Testa conexão com ambas as contas
        print("\n🔍 Testando dados...")
        old_mail = connect_imap(old_email, old_password)
        new_mail = connect_imap(new_email, new_password)
        if old_mail and new_mail:
            # Desconecta imediatamente após testar
            old_mail.logout()
            new_mail.logout()
            break
        else:
            print(Fore.RED + "\n❌ Dados inválidos! Por favor, digite novamente.\n" + Style.RESET_ALL)

    # Confirmação
    print(f"\n📧 De: {old_email}")
    print(f"📧 Para: {new_email}")
    confirm = input("✅ Confirma a migração? (s/n): ").lower()
    if confirm == "s":
        migrate_inbox(old_email, old_password, new_email, new_password)
    else:
        print("❌ Migração cancelada.")


def bulk_migration():
    """Gerencia migrações em massa"""
    print(Fore.LIGHTCYAN_EX + "🚀 MIGRAÇÃO EM MASSA" + Style.RESET_ALL)
    
    migration_list = []
    
    while True:
        print(f"\n📋 Migrações adicionadas: {len(migration_list)}")
        print("\n1. Adicionar nova migração")
        print("2. Ver migrações adicionadas")
        print("3. Executar todas as migrações")
        print("4. Voltar ao menu principal")
        
        opcao = input("\nEscolha uma opção (1-4): ")
        
        if opcao == "1":
            # Adicionar nova migração
            print(f"\n➕ Adicionando migração #{len(migration_list) + 1}")
            
            old_email = input_azul("Email de origem: ")
            old_password = pwinput.pwinput("Senha do email de origem: ", mask='*')
            new_email = input_azul("Email de destino: ")
            new_password = pwinput.pwinput("Senha do email de destino: ", mask='*')
            
            # Testa conexão
            print("\n🔍 Testando conexões...")
            old_mail = connect_imap(old_email, old_password)
            new_mail = connect_imap(new_email, new_password)
            
            if old_mail and new_mail:
                old_mail.logout()
                new_mail.logout()
                
                migration_list.append((old_email, old_password, new_email, new_password))
                print(Fore.GREEN + f"✅ Migração #{len(migration_list)} adicionada com sucesso!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "❌ Falha na validação. Migração não foi adicionada." + Style.RESET_ALL)
                
        elif opcao == "2":
            # Ver migrações adicionadas
            if not migration_list:
                print(Fore.YELLOW + "\n📭 Nenhuma migração foi adicionada ainda." + Style.RESET_ALL)
            else:
                print(f"\n📋 Migrações adicionadas ({len(migration_list)}):")
                for i, (old_email, _, new_email, _) in enumerate(migration_list, 1):
                    print(f"  {i}. {old_email} → {new_email}")
                    
        elif opcao == "3":
            # Executar migrações
            if not migration_list:
                print(Fore.YELLOW + "\n📭 Adicione pelo menos uma migração primeiro!" + Style.RESET_ALL)
            else:
                print(f"\n🚀 Executando {len(migration_list)} migrações...")
                confirm = input("✅ Confirma a execução? (s/n): ").lower()
                if confirm == "s":
                    migrate_bulk(migration_list)
                    migration_list = []  # Limpa a lista após execução
                else:
                    print("❌ Execução cancelada.")
                    
        elif opcao == "4":
            # Voltar ao menu principal
            if migration_list:
                print(Fore.YELLOW + f"\n⚠️ Você tem {len(migration_list)} migrações pendentes!" + Style.RESET_ALL)
                descartar = input("Deseja descartar? (s/n): ").lower()
                if descartar == "s":
                    print("📭 Migrações descartadas.")
                else:
                    continue
            break
        else:
            print(Fore.RED + "❌ Opção inválida!" + Style.RESET_ALL)


def input_azul(prompt):
    """Função para entrada colorida"""
    resposta = input(prompt)
    print(Fore.LIGHTBLUE_EX + resposta + Style.RESET_ALL)
    return resposta


if __name__ == "__main__":
    init(autoreset=True)
    print(Fore.LIGHTCYAN_EX + r"""
 ________  ________  ________  ___  _____ ______   ________  ___  ___          
|\   ____\|\   __  \|\   __  \|\  \|\   _ \  _   \|\   __  \|\  \|\  \         
\ \  \___|\ \  \|\  \ \  \|\  \ \  \ \  \\\__\ \  \ \  \|\  \ \  \ \  \        
 \ \  \    \ \  \\\  \ \   ____\ \  \ \  \\|__| \  \ \   __  \ \  \ \  \       
  \ \  \____\ \  \\\  \ \  \___|\ \  \ \  \    \ \  \ \  \ \  \ \  \ \  \____  
   \ \_______\ \_______\ \__\    \ \__\ \__\    \ \__\ \__\ \__\ \__\ \_______\
    \|_______|\|_______|\|__|     \|__|\|__|     \|__|\|__|\|__|\|__|\|_______|
                                                                               
                                                                               
""" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + "===== MIGRADOR DE EMAILS =====\n" + Style.RESET_ALL)

    # Loop principal para múltiplas sessões
    while True:
        print(Fore.LIGHTCYAN_EX + "MENU PRINCIPAL" + Style.RESET_ALL)
        print("\n1. Migração Individual (Email → Email)")
        print("2. Migração em Massa (Múltiplos Emails)")
        print("3. Sair do Programa")
        
        opcao_principal = input("\nEscolha uma opção (1-3): ")
        
        if opcao_principal == "1":
            individual_migration()
        elif opcao_principal == "2":
            bulk_migration()
        elif opcao_principal == "3":
            print(Fore.GREEN + "\n👋 Obrigado por usar o Migrador de Emails!" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "✨ Programa finalizado." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "❌ Opção inválida!" + Style.RESET_ALL)
        
        # Pergunta se quer continuar no programa
        if opcao_principal in ["1", "2"]:
            print(Fore.YELLOW + "\n" + "="*50 + Style.RESET_ALL)
            continuar = input(Fore.LIGHTCYAN_EX + "🔄 Deseja voltar ao menu principal? (s/n): " + Style.RESET_ALL).lower()
            if continuar != "s":
                print(Fore.GREEN + "\n👋 Obrigado por usar o Migrador de Emails!" + Style.RESET_ALL)
                print(Fore.LIGHTCYAN_EX + "✨ Programa finalizado." + Style.RESET_ALL)
                break
