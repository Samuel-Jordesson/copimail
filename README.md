 ________  ________  ________  ___  _____ ______   ________  ___  ___          
|\   ____\|\   __  \|\   __  \|\  \|\   _ \  _   \|\   __  \|\  \|\  \         
\ \  \___|\ \  \|\  \ \  \|\  \ \  \ \  \\\__\ \  \ \  \|\  \ \  \ \  \        
 \ \  \    \ \  \\\  \ \   ____\ \  \ \  \\|__| \  \ \   __  \ \  \ \  \       
  \ \  \____\ \  \\\  \ \  \___|\ \  \ \  \    \ \  \ \  \ \  \ \  \ \  \____  
   \ \_______\ \_______\ \__\    \ \__\ \__\    \ \__\ \__\ \__\ \__\ \_______\
    \|_______|\|_______|\|__|     \|__|\|__|     \|__|\|__|\|__|\|__|\|_______|

# 🚀 CopiMail - Sistema de Migração de Emails

Sistema profissional para migração de emails entre contas, com interface intuitiva e funcionalidades avançadas.

## ✨ Funcionalidades

- **Migração Individual**: Email para email com validação automática
- **Migração em Massa**: Múltiplas migrações simultâneas
- **Barras de Progresso**: Visualização em tempo real do progresso
- **Interface Colorida**: Experiência visual agradável
- **Validação Automática**: Testa conexões antes de executar
- **Preservação de Datas**: Mantém datas originais dos emails

## 🚀 Instalação Rápida

### 1. Baixar o Instalador
```bash
# Baixar o script de instalação
curl -O https://raw.githubusercontent.com/Samuel-Jordesson/copimail/main/install_copimail.py
```

### 2. Executar Instalação
```bash
# Instalar o sistema
python install_copimail.py
```

<<<<<<< HEAD
**✨ Barras de Progresso Elegantes**: A instalação mostra barras de progresso visuais para cada etapa, criando uma experiência de instalação profissional e agradável.
=======
<<<<<<< HEAD
**✨ Interface Limpa**: A instalação mostra apenas barras de progresso elegantes, sem mensagens verbosas.
=======
**✨ Barras de Progresso Elegantes**: A instalação mostra barras de progresso visuais para cada etapa, criando uma experiência de instalação profissional e agradável.
>>>>>>> 5be5edd (Adiciona arquivos do projeto)
>>>>>>> 14d72db (Adiciona arquivos do projeto)

**🔄 Dependências Automáticas**: O instalador instala automaticamente todas as dependências necessárias durante a instalação.

### 3. Usar o Sistema
```bash
# Executar CopiMail
copimail
```

**Nota**: No Windows, o PATH é configurado automaticamente. Após a instalação, reinicie o terminal/PowerShell para usar o comando `copimail`.

### 4. Testar Configuração (Opcional)
```bash
# Testar se o PATH foi configurado corretamente
python test_path_config.py
```

## 📋 Requisitos

- Python 3.6 ou superior
- Conexão com internet
- Contas de email com acesso IMAP

## 🔧 Configuração

### Servidores Suportados
- **Hostinger** (configurado por padrão)
- **Gmail** (requer configuração adicional)
- **Outlook** (requer configuração adicional)

### Configuração Personalizada
Para usar outros servidores, edite o arquivo `copimail.py`:

```python
IMAP_SERVER = "imap.seuservidor.com"
PORT = 993
```

## 📖 Como Usar

### Migração Individual
1. Escolha opção 1 no menu principal
2. Digite email e senha de origem
3. Digite email e senha de destino
4. Confirme a migração
5. Aguarde a conclusão

### Migração em Massa
1. Escolha opção 2 no menu principal
2. Adicione múltiplos pares de emails
3. Visualize a lista de migrações
4. Execute todas de uma vez
5. Acompanhe o progresso

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
copimail/
├── copimail.py          # Sistema principal
├── install_copimail.py  # Script de instalação
├── requirements.txt     # Dependências
├── version.json         # Informações de versão
├── test_path_config.py  # Script de teste do PATH
└── README.md           # Este arquivo
```

### Dependências
- `colorama`: Cores no terminal
- `pwinput`: Entrada mascarada de senhas
- `tqdm`: Barras de progresso

### Instalar Dependências de Desenvolvimento
```bash
pip install -r requirements.txt
```

## 🔄 Atualizações

Para atualizar o sistema:
```bash
# Executar instalador novamente
python install_copimail.py
```

## 🐛 Solução de Problemas

### Erro de Conexão
- Verifique se as credenciais estão corretas
- Confirme se o servidor IMAP está acessível
- Verifique se a porta 993 está liberada

### Erro de Dependências
```bash
# Reinstalar dependências
pip install --upgrade colorama pwinput tqdm
```

### Problemas no Windows
- O PATH é configurado automaticamente durante a instalação
- Se o comando `copimail` não funcionar, reinicie o terminal/PowerShell
- Execute como administrador se necessário para configurações de sistema

## 📝 Changelog

### v1.0.0 (2024-01-15)
- ✅ Versão inicial
- ✅ Migração individual e em massa
- ✅ Barras de progresso
- ✅ Interface colorida
- ✅ Validação automática
- ✅ Configuração automática do PATH no Windows
<<<<<<< HEAD
- ✅ Barras de progresso visuais para cada etapa da instalação
=======
<<<<<<< HEAD
- ✅ Interface de instalação limpa com barras de progresso
=======
- ✅ Barras de progresso visuais para cada etapa da instalação
>>>>>>> 5be5edd (Adiciona arquivos do projeto)
>>>>>>> 14d72db (Adiciona arquivos do projeto)
- ✅ Instalação automática de dependências

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

- **GitHub Issues**: [Abrir Issue](https://github.com/Samuel-Jordesson/copimail/issues)
- **Email**: seuemail@exemplo.com

## 🙏 Agradecimentos

- Comunidade Python
- Bibliotecas open source utilizadas
- Usuários que testaram e reportaram bugs

---

**Desenvolvido com ❤️ para facilitar a migração de emails**

