# Configuração MySQL para FSA

## ✅ Configuração SQLTools MySQL Concluída

A extensão SQLTools foi configurada para funcionar com MySQL ao invés de SQLite.

## 📋 Pré-requisitos

### 1. Instalar MySQL
- **Windows**: Baixe o MySQL Community Server
- **Ubuntu/Debian**: `sudo apt install mysql-server`
- **macOS**: `brew install mysql`

### 2. Instalar Extensões VS Code
- SQLTools (por Matheus Teixeira)
- SQLTools MySQL/MariaDB (por Matheus Teixeira)

### 3. Instalar Dependências Python
```bash
pip install -r requirements_mysql.txt
```

## 🔧 Configuração do MySQL

### 1. Iniciar MySQL
```bash
# Windows
net start mysql

# Linux/macOS
sudo systemctl start mysql
# ou
sudo service mysql start
```

### 2. Configurar Usuário e Senha
```sql
-- Conectar como root
mysql -u root -p

-- Criar usuário (opcional)
CREATE USER 'fsa_user'@'localhost' IDENTIFIED BY 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON fsa_teste.* TO 'fsa_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Atualizar Configurações
Edite os arquivos de configuração com suas credenciais:

**`.vscode/settings.json`** e **`.vscode/sqltools.json`**:
```json
{
    "name": "FSA MySQL Database",
    "driver": "MySQL",
    "server": "localhost",
    "port": 3306,
    "database": "fsa_teste",
    "username": "root",  // ou seu usuário
    "password": "sua_senha_aqui"  // sua senha
}
```

**`config_mysql.py`**:
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',  # ou seu usuário
    'password': 'sua_senha_aqui',  # sua senha
    'database': 'fsa_teste',
    'charset': 'utf8mb4'
}
```

## 🚀 Migração dos Dados

### 1. Executar Script de Migração
```bash
python migrate_to_mysql.py
```

Este script irá:
- ✅ Criar o banco `fsa_teste` no MySQL
- ✅ Criar todas as tabelas com estrutura otimizada
- ✅ Migrar todos os dados do SQLite para MySQL
- ✅ Configurar relacionamentos e índices

### 2. Verificar Migração
```sql
-- Conectar ao MySQL
mysql -u root -p fsa_teste

-- Verificar tabelas
SHOW TABLES;

-- Verificar dados
SELECT COUNT(*) FROM paciente;
SELECT COUNT(*) FROM estagiario;
SELECT COUNT(*) FROM agendamento;
```

## 🔄 Alternar entre SQLite e MySQL

### Para usar MySQL (padrão):
```python
# Em main.py, use:
from config_mysql import get_database_uri, get_database_config

app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config.update(get_database_config())
```

### Para voltar ao SQLite:
```python
# Em main.py, use:
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'fsa_teste.db')
```

## 📊 Vantagens do MySQL

- ✅ **Performance**: Mais rápido para consultas complexas
- ✅ **Escalabilidade**: Suporta mais usuários simultâneos
- ✅ **Recursos**: Triggers, stored procedures, views
- ✅ **Backup**: Ferramentas robustas de backup
- ✅ **Monitoramento**: Melhor visibilidade de performance
- ✅ **SQLTools**: Interface visual completa no VS Code

## 🔍 Consultas de Exemplo

```sql
-- Ver todos os pacientes
SELECT * FROM paciente;

-- Agendamentos com nomes
SELECT 
    a.id,
    p.nome as paciente,
    e.nome as estagiario,
    a.data_agendamento,
    a.status
FROM agendamento a
LEFT JOIN paciente p ON a.paciente_id = p.id
LEFT JOIN estagiario e ON a.estagiario_id = e.id;

-- Estatísticas
SELECT 
    'Pacientes' as tipo, COUNT(*) as total FROM paciente
UNION ALL
SELECT 'Estagiários', COUNT(*) FROM estagiario
UNION ALL
SELECT 'Agendamentos', COUNT(*) FROM agendamento;
```

## ⚠️ Troubleshooting

### Erro de Conexão
- Verifique se o MySQL está rodando
- Confirme usuário e senha
- Teste conexão: `mysql -u root -p`

### Erro de Driver
- Instale: `pip install PyMySQL mysql-connector-python`

### Erro de Permissão
- Verifique se o usuário tem acesso ao banco
- Execute: `GRANT ALL PRIVILEGES ON fsa_teste.* TO 'seu_usuario'@'localhost';`

## 🎯 Próximos Passos

1. ✅ Instalar MySQL
2. ✅ Instalar extensões VS Code
3. ✅ Configurar credenciais
4. ✅ Executar migração
5. ✅ Testar conexão no SQLTools
6. ✅ Atualizar aplicação Flask para MySQL

Agora você tem uma configuração completa MySQL com SQLTools! 🎉
