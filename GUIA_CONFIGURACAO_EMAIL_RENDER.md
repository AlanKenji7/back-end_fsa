# 📧 Guia Completo: Configurar Email no Render

## 🔍 Problema Identificado

Quando você sobe o código para o Render, os emails não chegam aos pacientes porque:

1. **Variáveis de ambiente não estão configuradas no Render**
2. **Credenciais de email não estão sendo carregadas corretamente**
3. **Possível problema com senha de app do Gmail expirada ou inválida**

## ✅ Correções Aplicadas no Código

### 1. Bug Crítico Corrigido
- **Antes**: A função retornava `True` mesmo sem credenciais configuradas
- **Agora**: Retorna `False` e registra erro detalhado quando credenciais estão ausentes

### 2. Logging Melhorado
- Logs detalhados mostram exatamente o que está acontecendo
- Erros específicos com dicas de como resolver
- Verificação de configuração ao iniciar o servidor

### 3. Remoção de Senha Hardcoded
- Senha foi removida do código por segurança
- Agora usa apenas variáveis de ambiente

## 📋 Passo a Passo para Configurar no Render

### Passo 1: Acessar o Painel do Render

1. Acesse https://dashboard.render.com
2. Faça login na sua conta
3. Selecione o seu serviço (web service)

### Passo 2: Configurar Variáveis de Ambiente

1. No painel do seu serviço, vá em **"Environment"** no menu lateral
2. Clique em **"Add Environment Variable"**
3. Adicione as seguintes variáveis:

#### Variável 1: MAIL_USERNAME
```
Key: MAIL_USERNAME
Value: fundacaofsaacex@gmail.com
```

#### Variável 2: MAIL_PASSWORD
```
Key: MAIL_PASSWORD
Value: [sua senha de app do Gmail - ver instruções abaixo]
```

#### Variável 3: SECRET_KEY (se ainda não tiver)
```
Key: SECRET_KEY
Value: [gere uma chave secreta forte]
```

### Passo 3: Obter Senha de App do Gmail

**⚠️ IMPORTANTE**: Você NÃO pode usar sua senha normal do Gmail. Precisa criar uma "Senha de App".

#### Como criar uma Senha de App:

1. **Ative a Verificação em Duas Etapas** (se ainda não tiver):
   - Acesse: https://myaccount.google.com/security
   - Ative "Verificação em duas etapas"

2. **Crie uma Senha de App**:
   - Acesse: https://myaccount.google.com/apppasswords
   - Selecione "Email" como app
   - Selecione "Outro (Nome personalizado)" como dispositivo
   - Digite "Render" como nome
   - Clique em "Gerar"
   - **Copie a senha gerada** (16 caracteres, sem espaços)

3. **Use a senha no Render**:
   - Cole a senha de 16 caracteres no valor de `MAIL_PASSWORD`
   - **Não adicione espaços** - a senha deve ser contínua

### Passo 4: Verificar Configuração

1. Após adicionar as variáveis, o Render fará um novo deploy automaticamente
2. Aguarde o deploy terminar
3. Acesse os logs do serviço no Render
4. Você deve ver uma mensagem como:

```
============================================================
✅ Configurações de email detectadas
✅ MAIL_USERNAME: fundacaofsaacex@gmail.com
✅ MAIL_SERVER: smtp.gmail.com:587
============================================================
```

Se ver uma mensagem de aviso sobre credenciais ausentes, as variáveis não foram configuradas corretamente.

### Passo 5: Testar o Envio de Email

1. Após o deploy, acesse a rota de teste:
   ```
   https://seu-app.render.com/teste-email
   ```

2. Você deve receber um JSON com o status da configuração

3. Verifique a caixa de entrada do email `fundacaofsaacex@gmail.com`
   - **Verifique também a pasta de SPAM/LIXO ELETRÔNICO**
   - Gmail pode marcar emails como spam inicialmente

## 🔍 Como Diagnosticar Problemas

### Problema 1: "Credenciais não configuradas"

**Sintoma**: Logs mostram "⚠️ Configurações de email ausentes!"

**Solução**:
1. Verifique se as variáveis `MAIL_USERNAME` e `MAIL_PASSWORD` estão configuradas no Render
2. Certifique-se de que os nomes estão exatamente assim (maiúsculas)
3. Reinicie o serviço no Render após adicionar as variáveis

### Problema 2: "Authentication Error" ou "535"

**Sintoma**: Erro de autenticação ao tentar enviar email

**Solução**:
1. Verifique se está usando **senha de APP**, não senha normal
2. Gere uma nova senha de app no Google
3. Certifique-se de que a senha não tem espaços
4. Verifique se a verificação em duas etapas está ativada

### Problema 3: "Connection Timeout"

**Sintoma**: Erro de conexão ao servidor SMTP

**Solução**:
1. Verifique se a porta 587 não está bloqueada
2. O Render permite conexões de saída, então isso é raro
3. Verifique os logs para mais detalhes

### Problema 4: "Email enviado mas não chega"

**Sintoma**: Logs mostram sucesso, mas email não aparece

**Solução**:
1. **Verifique a pasta de SPAM** - muito comum!
2. Verifique se o email do destinatário está correto
3. Gmail pode marcar emails como spam - marque como "não é spam"
4. Verifique se o email não foi bloqueado pelo provedor

## 📊 Verificar Logs no Render

1. No painel do Render, vá em **"Logs"**
2. Procure por mensagens relacionadas a email
3. Mensagens de sucesso:
   ```
   ✅ Email enviado com sucesso para paciente@email.com
   ```

4. Mensagens de erro:
   ```
   ❌ ERRO CRÍTICO AO ENVIAR EMAIL!
   ❌ Tipo do erro: SMTPAuthenticationError
   ```

## 🧪 Testar Localmente

Para testar localmente antes de fazer deploy:

1. Crie um arquivo `.env` na raiz do projeto:
```env
MAIL_USERNAME=fundacaofsaacex@gmail.com
MAIL_PASSWORD=sua_senha_de_app_aqui
SECRET_KEY=sua_chave_secreta_aqui
```

2. Execute o servidor:
```bash
python main.py
```

3. Acesse: http://localhost:5000/teste-email

4. Verifique os logs no terminal

## ✅ Checklist Final

Antes de considerar o problema resolvido, verifique:

- [ ] Variáveis `MAIL_USERNAME` e `MAIL_PASSWORD` configuradas no Render
- [ ] Senha de APP do Gmail gerada e configurada (não senha normal)
- [ ] Verificação em duas etapas ativada no Gmail
- [ ] Deploy completo no Render concluído
- [ ] Logs mostram "✅ Configurações de email detectadas"
- [ ] Rota `/teste-email` retorna status "ok"
- [ ] Email de teste chegou na caixa de entrada (verificar SPAM também)
- [ ] Email real para paciente foi enviado e chegou

## 📞 Se Ainda Não Funcionar

1. **Verifique os logs completos** no Render quando tentar enviar um email
2. **Copie a mensagem de erro completa** dos logs
3. **Teste a rota `/teste-email`** e veja o retorno JSON
4. **Verifique se a senha de app não expirou** (gere uma nova se necessário)
5. **Teste enviando para seu próprio email** primeiro

## 🔒 Segurança

- **Nunca** commite senhas no código
- **Sempre** use variáveis de ambiente
- **Nunca** compartilhe senhas de app
- **Rotacione** senhas de app periodicamente
- **Use** senhas de app diferentes para desenvolvimento e produção

## 📝 Notas Importantes

- O envio de email é **assíncrono** (em background) para evitar timeout
- Emails podem levar alguns segundos para serem enviados
- Gmail pode marcar emails como spam inicialmente - isso é normal
- Verifique sempre a pasta de SPAM antes de reportar problema
- Logs detalhados ajudam a diagnosticar problemas rapidamente

---

**Última atualização**: Após as correções aplicadas no código
**Status**: Pronto para configurar no Render

