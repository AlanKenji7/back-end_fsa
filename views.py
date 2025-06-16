# views.py
from main import app # Importa o aplicativo Flask principal
from db import db
from models import Paciente, Estagiario, Disponibilidade, Agendamento
from flask import render_template, request, redirect, url_for, flash, session,jsonify, current_app
import datetime # Adicionado para conversão de data
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_ou_username = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') 

        print(f"DEBUG: Tentativa de login para E-mail/Usuário: '{email_ou_username}'")
        print(f"DEBUG: Senha fornecida: '{password}' (não mostre isso em produção!)")

        # 1. Tentar encontrar um Estagiário
        user_estagiario = Estagiario.query.filter_by(emailfsa=email_ou_username).first()
        
        if user_estagiario:
            print(f"DEBUG: Estagiário encontrado: ID={user_estagiario.id}, Nome={user_estagiario.nome}, EmailFSA={user_estagiario.emailfsa}")
            print(f"DEBUG: Senha hash do banco para estagiário: {user_estagiario.senha}")
            
            if check_password_hash(user_estagiario.senha, password):
                print("DEBUG: Senha do estagiário CORRETA!")
                session['logged_in'] = True
                session['user_id'] = user_estagiario.id
                session['user_type'] = 'estagiario'
                session['nome_usuario'] = user_estagiario.nome
                flash('Login de estagiário bem-sucedido!', 'success')
                return redirect(url_for('aba_estagiario')) 
            else:
                print("DEBUG: Senha do estagiário INCORRETA.")
                flash('E-mail/Nome de usuário ou senha inválidos.', 'error')
                # Renderiza login.html novamente se a senha estiver incorreta
                return render_template('login.html')

        # 2. Se não encontrou estagiário ou a senha do estagiário estava errada, tentar encontrar um Paciente
        else: # Só tenta paciente se não encontrou estagiário com o email
            print("DEBUG: Nenhum Estagiário encontrado com este e-mail/usuário. Tentando como Paciente.")
            user_paciente = Paciente.query.filter_by(email=email_ou_username).first()

            if user_paciente:
                print(f"DEBUG: Paciente encontrado: ID={user_paciente.id}, Nome={user_paciente.nome}, Email={user_paciente.email}")
                print(f"DEBUG: Senha hash do banco para paciente: {user_paciente.senha}")
                
                if check_password_hash(user_paciente.senha, password):
                    print("DEBUG: Senha do paciente CORRETA!")
                    session['logged_in'] = True
                    session['user_id'] = user_paciente.id
                    session['user_type'] = 'paciente'
                    session['nome_usuario'] = user_paciente.nome
                    flash('Login de paciente bem-sucedido!', 'success')
                    return redirect(url_for('agendamentos')) 
                else:
                    print("DEBUG: Senha do paciente INCORRETA.")
                    flash('E-mail/Nome de usuário ou senha inválidos.', 'error')
                    # Renderiza login.html novamente se a senha estiver incorreta
                    return render_template('login.html')
            else:
                print("DEBUG: Nenhum Paciente encontrado com este e-mail/usuário.")
                flash('E-mail/Nome de usuário ou senha inválidos.', 'error')
                # Renderiza login.html novamente se nenhum usuário foi encontrado
                return render_template('login.html')
        
    # Se o método for GET (primeiro acesso à página) ou algum erro acima impediu o redirect
    print("DEBUG: Renderizando login.html (Método GET ou falha no POST).")
    return render_template('login.html')






# Rota de logout
@app.route('/logout')
def logout():
    session.clear() # Limpa todas as informações da sessão
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# Rota raiz (pode redirecionar para a página de login, por exemplo)
@app.route('/')
def index():
    # Isso pode ser ajustado para direcionar para uma landing page ou o próprio login
    return redirect(url_for('login'))
























# Rota de paciente
@app.route('/cadastroPaciente', methods=['GET', 'POST'])
def registrar_paciente():
    if request.method == 'POST':
        print("DEBUG: Recebido POST para /cadastroPaciente") # DEBUG
        dados_paciente = {
            'nome': request.form['nomeForm'],
            'data_nascimento': request.form['dataNascimentoForm'],
            'genero': request.form['generoForm'],
            'cpf': request.form['cpfForm'],
            'telefone': request.form['TelefoneForm'],
            'email': request.form['emailForm'],
            'endereco': request.form['enderecoForm'],
            'numero_casa': request.form['numeroCasaForm']
        }
        session['dados_paciente'] = dados_paciente
        flash('Dados do paciente salvos temporariamente. Agora crie sua senha.', 'info')
        print("DEBUG: Redirecionando para criar_senha") # DEBUG
        return redirect(url_for('criar_senha'))
    
    messages = session.pop('_flashes', [])
    return render_template("cadastroPaciente.html", messages=messages)

@app.route('/criarSenha', methods=['GET', 'POST'])
def criar_senha():
    if request.method == 'POST':
        print("DEBUG: Recebido POST para /criarSenha") # DEBUG
        if 'dados_paciente' not in session:
            flash('Por favor, preencha os dados do paciente primeiro.', 'error')
            print("DEBUG: dados_paciente não encontrado na sessão. Redirecionando para registrar_paciente.") # DEBUG
            return redirect(url_for('registrar_paciente'))

        print(f"DEBUG: Conteúdo da sessão ao entrar em criar_senha (POST): {session.get('dados_paciente')}") # DEBUG

        senha = request.form['password']
        confirmar_senha = request.form['confirm_password']

        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'error')
            messages = session.pop('_flashes', [])
            print("DEBUG: Senhas não coincidem.") # DEBUG
            return render_template("criarSenha.html", messages=messages)
        
        if not (8 <= len(senha) <= 20):
            flash('A senha deve ter entre 8 e 20 caracteres.', 'error')
            messages = session.pop('_flashes', [])
            print("DEBUG: Senha fora do tamanho permitido.") # DEBUG
            return render_template("criarSenha.html", messages=messages)
        
        print("DEBUG: Senha e confirmação válidas. Tentando criar paciente.") # DEBUG
        hashed_senha = senha 

        dados_paciente = session['dados_paciente']

        # CONVERSÃO DA DATA: CORRIGIDO AQUI
        try:
            data_nascimento_obj = datetime.datetime.strptime(dados_paciente['data_nascimento'], '%Y-%m-%d').date()
        except ValueError as e:
            flash(f'Formato de data de nascimento inválido: {e}', 'error')
            messages = session.pop('_flashes', [])
            print(f"DEBUG: Erro no formato da data de nascimento: {e}") # DEBUG
            return render_template("criarSenha.html", messages=messages)

        novo_paciente = Paciente(
            nome=dados_paciente['nome'],
            data_nascimento=data_nascimento_obj, # Usando o objeto de data
            genero=dados_paciente['genero'],
            cpf=dados_paciente['cpf'],
            telefone=dados_paciente['telefone'],
            email=dados_paciente['email'],
            endereco=dados_paciente['endereco'],
            numero_casa=dados_paciente['numero_casa'],
            senha=hashed_senha
        )
        print(f"DEBUG: Objeto Paciente criado: {novo_paciente}") # DEBUG

        try:
            db.session.add(novo_paciente)
            print("DEBUG: Paciente adicionado à sessão do DB.") # DEBUG
            db.session.commit()
            print("DEBUG: db.session.commit() executado com sucesso. Dados salvos.") # DEBUG
            flash('Paciente cadastrado com sucesso!', 'success')
            session.pop('dados_paciente', None) 
            # CORRIGIDO: url_for() espera o nome da função, não o nome do arquivo HTML
            print("DEBUG: Redirecionando para a rota agendamentos.") # DEBUG
            return redirect(url_for('aba_pacientes'))
        except Exception as e:
            db.session.rollback()
            print(f"DEBUG: ERRO DURANTE db.session.add/commit: {e}") # DEBUG CRÍTICO!
            flash(f'Ocorreu um erro ao cadastrar o paciente: {e}', 'error')
            messages = session.pop('_flashes', []) 
            return render_template("criarSenha.html", messages=messages)
            
    messages = session.pop('_flashes', [])
    return render_template("criarSenha.html", messages=messages)

# Rota para a página de agendamentos de triagem
@app.route('/aba_pacientes')
def aba_pacientes():
    print("DEBUG: Acessando a rota /aba_pacientes.") # DEBUG
    messages = session.pop('_flashes', []) # Para exibir mensagens flash se houver
    return render_template("aba_pacientes.html", messages=messages) # Assumindo que você tem agendamentos.html



# Rota para o formulário de cadastro do aluno (primeira etapa)
@app.route('/cadastroaluno', methods=['GET', 'POST'])
def tela_cadastro_aluno():
    if request.method == 'POST':
        print("DEBUG: Recebido POST para /cadastroaluno")
        dados_Estagiario = {
            'nome': request.form['nomeForm'],
            'data_nascimento': request.form['dataNascimentoForm'],
            'cpf': request.form['cpfForm'],
            'telefone_aluno': request.form['Telefone_alunoForm'],
            'emailfsa': request.form['emailFsaForm'],
            'RA': request.form['raForm'],
            'curso_periodo': request.form['cursoPeriodoForm']
        }
        session['dados_Estagiario'] = dados_Estagiario
        flash('Dados do Estagiário salvos temporariamente. Agora crie sua senha.', 'info')
        print("DEBUG: Redirecionando para criar_senha_aluno.") # Nome da rota corrigido
        return redirect(url_for('criar_senha_aluno'))
    
    print("DEBUG: Acessando a rota /cadastroaluno (GET)")
    messages = session.pop('_flashes', [])
    return render_template("cadastroaluno.html", messages=messages)


@app.route('/criarSenha_aluno', methods=['GET', 'POST'])
def criar_senha_aluno():
    # Primeira verificação: se 'dados_Estagiario' não está na sessão (primeiro acesso ou acesso direto)
    if 'dados_Estagiario' not in session:
        flash('Por favor, preencha os dados do Estagiário primeiro.', 'error')
        print("DEBUG: dados_Estagiario não encontrado na sessão. Redirecionando para tela_cadastro_aluno.")
        return redirect(url_for('tela_cadastro_aluno'))

    # Se o método for POST (o usuário submeteu o formulário de senha)
    if request.method == 'POST':
        senha = request.form['password']
        confirmar_senha = request.form['confirm_password']

        # Validação de senhas
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'error')
            # Renderiza a mesma página com a mensagem de erro
            return render_template("criarSenha_aluno.html", messages=session.pop('_flashes', []))
        
        if not (8 <= len(senha) <= 20):
            flash('A senha deve ter entre 8 e 20 caracteres.', 'error')
            # Renderiza a mesma página com a mensagem de erro
            return render_template("criarSenha_aluno.html", messages=session.pop('_flashes', []))
        
        hashed_senha = generate_password_hash(senha, method='pbkdf2:sha256')

        dados_Estagiario = session['dados_Estagiario']

        # Tenta converter a data de nascimento
        try:
            data_nascimento_obj = datetime.datetime.strptime(dados_Estagiario['data_nascimento'], '%Y-%m-%d').date()
        except ValueError as e:
            flash(f'Formato de data de nascimento inválido: {e}', 'error')
            print(f"DEBUG: ERRO de formato de data: {e}") 
            # Renderiza a mesma página com a mensagem de erro
            return render_template("criarSenha_aluno.html", messages=session.pop('_flashes', []))

       #py (trecho da função criar_senha_aluno)

        novo_Estagiario = Estagiario(
            nome=dados_Estagiario['nome'],
            data_nascimento=data_nascimento_obj,
            RA=dados_Estagiario['RA'],
            cpf=dados_Estagiario['cpf'],
            # ALTERE ESTA LINHA:
            telefone_aluno=dados_Estagiario['telefone_aluno'], # <-- Use 'telefone_aluno' aqui
            emailfsa=dados_Estagiario['emailfsa'],
            curso_periodo=dados_Estagiario['curso_periodo'],
            senha=hashed_senha
        )
        
        print(f"DEBUG: Objeto Estagiário criado: {novo_Estagiario}")

        # Tenta adicionar e commitar no banco de dados
        try:
            print("DEBUG: Tentando adicionar novo_Estagiario ao banco de dados.") 
            db.session.add(novo_Estagiario)
            print("DEBUG: Objeto adicionado à sessão. Tentando commit...") 
            db.session.commit()
            print("DEBUG: Commit realizado com sucesso!") 
            flash('Estagiário cadastrado com sucesso!', 'success')
            session.pop('dados_Estagiario', None) # Limpa os dados do estagiário da sessão

            # ESTE É O ÚNICO RETORNO ESPERADO EM CASO DE SUCESSO DO POST
            return redirect(url_for('aba_estagiario')) 
        except Exception as e:
            db.session.rollback()
            print(f"DEBUG: ERRO NO BANCO DE DADOS: {e}") 
            flash(f'Ocorreu um erro ao cadastrar o estagiário: {e}', 'error')
            # Renderiza a mesma página com a mensagem de erro do banco de dados
            return render_template("criarSenha_aluno.html", messages=session.pop('_flashes', []))
            
    # Se o método for GET (ou seja, é o primeiro acesso à página de criação de senha)
    # ou se a validação inicial de 'dados_Estagiario' na sessão falhou
    messages = session.pop('_flashes', [])
    return render_template("criarSenha_aluno.html", messages=messages)
            
# Rota para a aba do estagiário
@app.route('/aba_estagiario')
def aba_estagiario():
    print("DEBUG: Acessando a rota /aba_estagiario.")
    messages = session.pop('_flashes', [])
    return render_template("aba_estagiario.html", messages=messages)

@app.route('/disponibilidade', methods=['GET', 'POST'])
def disponibilidade():
    if 'user_type' not in session or session['user_type'] != 'estagiario':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('login'))

    estagiario_id = session['user_id']
    
    if request.method == 'POST':
        dia_semana = request.form.get('dia_semana')
        horario_inicio = request.form.get('horario_inicio')
        horario_fim = request.form.get('horario_fim')

        if not all([dia_semana, horario_inicio, horario_fim]):
            flash('Todos os campos são obrigatórios.', 'error')
        else:
            try:
                inicio_time = datetime.datetime.strptime(horario_inicio, '%H:%M').time()
                fim_time = datetime.datetime.strptime(horario_fim, '%H:%M').time()

                nova_disponibilidade = Disponibilidade(
                    estagiario_id=estagiario_id,
                    dia_semana=dia_semana,
                    horario_inicio=inicio_time,
                    horario_fim=fim_time
                )
                db.session.add(nova_disponibilidade)
                db.session.commit()
                flash('Disponibilidade adicionada com sucesso!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao adicionar disponibilidade: {e}', 'error')
        
        return redirect(url_for('disponibilidade'))

    disponibilidades = Disponibilidade.query.filter_by(estagiario_id=estagiario_id).order_by(Disponibilidade.dia_semana).all()
    return render_template('disponibilidades.html', disponibilidades=disponibilidades)

@app.route('/remover_disponibilidade/<int:id>', methods=['POST'])
def remover_disponibilidade(id):
    if 'user_type' not in session or session['user_type'] != 'estagiario':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('login'))

    disponibilidade = Disponibilidade.query.get_or_404(id)

    if disponibilidade.estagiario_id != session['user_id']:
        flash('Você não tem permissão para remover esta disponibilidade.', 'error')
        return redirect(url_for('disponibilidade'))

    try:
        db.session.delete(disponibilidade)
        db.session.commit()
        flash('Disponibilidade removida com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover disponibilidade: {e}', 'error')

    return redirect(url_for('disponibilidade'))





# Rota para listar pacientes (para depuração)
@app.route('/listar_pacientes')
def listar_pacientes():
    print("DEBUG: Acessando a rota /listar_pacientes.") # DEBUG
    pacientes = Paciente.query.all()
    print(f"DEBUG: Pacientes encontrados no DB: {pacientes}") # DEBUG
    messages = session.pop('_flashes', [])
    return render_template('listar_pacientes.html', pacientes=pacientes, messages=messages)
@app.route('/solicitar_triagem', methods=['POST'])
def solicitar_triagem():
    if 'user_type' not in session or session['user_type'] != 'paciente':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('login'))

    paciente_id = session['user_id']
    
    # Verifica se já existe uma solicitação pendente
    solicitacao_existente = Agendamento.query.filter_by(paciente_id=paciente_id, status='solicitado').first()
    if solicitacao_existente:
        flash('Você já possui uma solicitação de triagem pendente.', 'warning')
        return redirect(url_for('meus_agendamentos'))

    novo_agendamento = Agendamento(
        paciente_id=paciente_id,
        status='solicitado'
    )
    
    try:
        db.session.add(novo_agendamento)
        db.session.commit()
        flash('Solicitação de triagem enviada com sucesso! Aguarde um estagiário aceitar.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao solicitar triagem: {e}', 'error')

    return redirect(url_for('meus_agendamentos'))

@app.route('/meus_agendamentos')
def meus_agendamentos():
    if 'user_type' not in session or session['user_type'] != 'paciente':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('login'))

    paciente_id = session['user_id']
    agendamentos = Agendamento.query.filter_by(paciente_id=paciente_id).order_by(Agendamento.data_solicitacao.desc()).all()
    
    return render_template('meus_agendamentos.html', agendamentos=agendamentos)

@app.route('/confirmar_presenca/<int:id>', methods=['POST'])
def confirmar_presenca(id):
    if 'user_type' not in session or session['user_type'] != 'paciente':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('login'))

    agendamento = Agendamento.query.get_or_404(id)

    if agendamento.paciente_id != session['user_id']:
        flash('Você não tem permissão para confirmar este agendamento.', 'error')
        return redirect(url_for('meus_agendamentos'))

    if agendamento.status != 'aceito':
        flash('Este agendamento não pode ser confirmado.', 'warning')
        return redirect(url_for('meus_agendamentos'))

    agendamento.status = 'confirmado'
    try:
        db.session.commit()
        flash('Presença confirmada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao confirmar presença: {e}', 'error')

    return redirect(url_for('meus_agendamentos'))
@app.route('/solicitacoes_triagem')
def solicitacoes_triagem():
    if 'user_type' not in session or session['user_type'] != 'estagiario':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('login'))

    solicitacoes = Agendamento.query.filter_by(status='solicitado').order_by(Agendamento.data_solicitacao.asc()).all()
    return render_template('solicitacoes_triagem.html', solicitacoes=solicitacoes)

@app.route('/aceitar_triagem/<int:id>', methods=['POST'])
def aceitar_triagem(id):
    if 'user_type' not in session or session['user_type'] != 'estagiario':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('login'))

    agendamento = Agendamento.query.get_or_404(id)
    estagiario_id = session['user_id']

    data_agendamento_str = request.form.get('data_agendamento')
    horario_agendamento_str = request.form.get('horario_agendamento')

    if not data_agendamento_str or not horario_agendamento_str:
        flash('Data e horário do agendamento são obrigatórios.', 'error')
        return redirect(url_for('solicitacoes_triagem'))

    try:
        data_agendamento = datetime.datetime.strptime(data_agendamento_str, '%Y-%m-%d').date()
        horario_agendamento = datetime.datetime.strptime(horario_agendamento_str, '%H:%M').time()
    except ValueError:
        flash('Formato de data ou horário inválido.', 'error')
        return redirect(url_for('solicitacoes_triagem'))

    agendamento.estagiario_id = estagiario_id
    agendamento.data_agendamento = data_agendamento
    agendamento.horario_agendamento = horario_agendamento
    agendamento.status = 'aceito'

    try:
        db.session.commit()
        flash('Triagem aceita e agendada com sucesso! O paciente precisa confirmar a presença.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao aceitar a triagem: {e}', 'error')

    return redirect(url_for('solicitacoes_triagem'))