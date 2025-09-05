# Configuração SQLTools SQLite

## ✅ Configuração Concluída

A extensão SQLTools SQLite foi configurada para conectar ao banco de dados `fsa_teste.db`.

## 📋 Como Usar

### 1. Instalar a Extensão
- Abra o VS Code
- Vá em Extensions (Ctrl+Shift+X)
- Procure por "SQLTools" e "SQLTools SQLite"
- Instale ambas as extensões

### 2. Conectar ao Banco
- Abra o painel SQLTools (ícone de banco de dados na barra lateral)
- Você verá a conexão "FSA Teste Database"
- Clique em "Connect" para conectar

### 3. Visualizar Dados
- Expanda a conexão para ver as tabelas:
  - `paciente` (10 registros)
  - `estagiario` (2 registros) 
  - `agendamento` (8 registros)
  - `disponibilidade` (0 registros)
  - `alembic_version` (controle de versão)

### 4. Executar Consultas
- Clique com botão direito em uma tabela
- Selecione "Show Table Records" para ver os dados
- Ou use "New SQL File" para escrever consultas personalizadas

## 🔧 Arquivos de Configuração

- `.vscode/settings.json` - Configuração principal
- `.vscode/sqltools.json` - Configuração alternativa

## 📊 Estrutura do Banco

### Tabela `paciente`
- id, nome, data_nascimento, genero, cpf, telefone, email, endereco, numero_casa, senha

### Tabela `estagiario` 
- id, nome, data_nascimento, RA, cpf, telefone_aluno, emailfsa, curso_periodo, senha

### Tabela `agendamento`
- id, paciente_id, estagiario_id, data_solicitacao, data_agendamento, status, observacoes

### Tabela `disponibilidade`
- id, estagiario_id, data, hora_inicio, hora_fim

## ⚠️ Importante

- O banco de dados está localizado em `./instance/fsa_teste.db`
- Certifique-se de que o caminho está correto no seu sistema
- Se houver problemas de conexão, verifique se o arquivo existe e tem permissões de leitura

