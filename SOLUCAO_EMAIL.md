# 🔧 Solução para Problema de Envio de Emails

## ✅ Correções Aplicadas

### 1. **Bug Crítico Corrigido**
- **Problema**: A função retornava `True` mesmo quando não havia credenciais configuradas
- **Solução**: Agora retorna `False` corretamente quando credenciais estão ausentes
- **Arquivo**: `email_utils.py` linhas 51-56

### 2. **Logging Melhorado**
- Adicionados logs detalhados para diagnóstico
- Erros agora mostram tipo, mensagem e traceback completo
- Logs indicam claramente quando credenciais estão ausentes

### 3. **Rota de Diagnóstico Criada**
- Nova rota `/teste-email` para testar configuração
- Mostra status de todas as configurações de email
- Testa envio real de email

## 📋 Como Configurar o Email

### Para Desenvolvimento Local:

1. **Crie um arquivo `.env` na raiz do projeto:**

```env
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_senha_de_app_aqui
```

2. **Importante - Senha de App do Gmail:**
   - NÃO use sua senha normal do Gmail
   - Você precisa criar uma "Senha de App" no Google:
     1. Acesse: https://myaccount.google.com/security
     2. Ative "Verificação em duas etapas" (se ainda não tiver)
     3. Vá em "Senhas de app"
     4. Crie uma nova senha de app para "Email"
     5. Use essa senha no `.env` (sem espaços)

### Para Produção (Render):

1. No painel do Render, vá em **Environment Variables**
2. Adicione:
   - `MAIL_USERNAME` = seu email Gmail
   - `MAIL_PASSWORD` = senha de app do Gmail
   - `SECRET_KEY` = uma chave secreta forte

## 🧪 Como Testar

### 1. Teste de Diagnóstico:
Acesse no navegador ou via curl:
```
http://localhost:5000/teste-email
```

Isso vai mostrar:
- Status das configurações
- Se credenciais estão configuradas
- Tentativa de envio de email de teste

### 2. Verificar Logs:
Quando tentar enviar um email, verifique os logs do servidor. Você verá:
- ✅ Se o email foi enviado com sucesso
- ❌ Se houve erro, com detalhes completos

### 3. Verificar Caixa de Entrada:
- Verifique a caixa de entrada do email
- Verifique também a pasta de **SPAM/LIXO ELETRÔNICO**
- Gmail pode marcar emails como spam inicialmente

## 🔍 Problemas Comuns e Soluções

### Problema: "Credenciais não configuradas"
**Solução**: 
- Verifique se o arquivo `.env` existe na raiz do projeto
- Verifique se as variáveis estão escritas corretamente
- Reinicie o servidor após criar/modificar o `.env`

### Problema: "Erro de autenticação"
**Solução**:
- Use senha de APP, não senha normal do Gmail
- Verifique se a verificação em duas etapas está ativada
- Gere uma nova senha de app

### Problema: "Email não chega"
**Solução**:
- Verifique pasta de SPAM
- Verifique se o email do destinatário está correto
- Verifique logs do servidor para erros específicos
- Teste enviando para seu próprio email primeiro

### Problema: "Connection timeout"
**Solução**:
- Verifique sua conexão com internet
- Verifique se porta 587 não está bloqueada
- Tente usar porta 465 com SSL (requer mudança no config.py)

## 📝 Exemplo de Logs de Sucesso

```
📧 Tentando enviar email para: paciente@email.com
📧 Usando servidor: smtp.gmail.com:587
📧 Remetente: seu_email@gmail.com
✅ Email de confirmação de consulta enviado com sucesso para paciente@email.com
```

## 📝 Exemplo de Logs de Erro

```
❌ CREDENCIAIS DE EMAIL NÃO CONFIGURADAS!
MAIL_USERNAME: NÃO CONFIGURADO
MAIL_PASSWORD: NÃO CONFIGURADO
Configure as variáveis de ambiente MAIL_USERNAME e MAIL_PASSWORD
```

## 🚀 Próximos Passos

1. Configure as variáveis de ambiente conforme instruções acima
2. Teste usando a rota `/teste-email`
3. Verifique os logs para confirmar que está funcionando
4. Teste o fluxo completo de confirmação de consulta

## 📞 Suporte

Se ainda tiver problemas:
1. Verifique os logs completos do servidor
2. Teste a rota `/teste-email` e veja o retorno JSON
3. Verifique se todas as dependências estão instaladas: `pip install -r requirements.txt`

