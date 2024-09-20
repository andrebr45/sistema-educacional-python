from flask import Flask, redirect, url_for, render_template, request, session, flash, send_file, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import fitz
import locale
import bcrypt
import json
from io import BytesIO
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'db1.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime=timedelta(minutes=35)
app.config['UPLOAD_FOLDER'] = '/uploads'

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))  # Armazena o hash da senha
    data = db.Column(db.String(10))
    hora = db.Column(db.String(8))
    situacao = db.Column(db.String(8))
    nivel_acesso = db.Column(db.String(100))
    genero = db.Column(db.String(100))
    cpf = db.Column(db.String(100))
    data_nascimento = db.Column(db.String(100))
    matricula = db.Column(db.String(100))
    usuario = db.Column(db.String(100))
    lotacao = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    local_trabalho = db.Column(db.String(100))
    logradouro = db.Column(db.String(100))
    numero = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    cep = db.Column(db.String(100))

    def __init__(self, name, telefone, email, senha, data, hora, genero, cpf, data_nascimento, matricula, usuario, lotacao, cargo, local_trabalho, situacao, nivel_acesso, logradouro, numero, bairro, cidade, estado, cep):
        self.name = name
        self.telefone = telefone
        self.email = email
        self.senha = self.generate_password_hash(senha)  # Gera e armazena o hash da senhagenerate_password_hash(senha)  # Gera e armazena o hash da senha
        self.data = data
        self.hora = hora
        self.situacao = situacao
        self.nivel_acesso = nivel_acesso
        self.genero = genero
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.matricula = matricula
        self.usuario = usuario
        self.lotacao = lotacao
        self.cargo = cargo
        self.local_trabalho = local_trabalho
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

    def generate_password_hash(self, senha):
        return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_senha(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha.encode('utf-8'))

class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    login_date = db.Column(db.String(10))  # Data do login
    login_time = db.Column(db.String(8))   # Hora do login

    user = db.relationship('users', backref=db.backref('logins', lazy=True))

class Escola(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    codigo = db.Column(db.String(100))
    categoria = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    qnt_alunos = db.Column(db.Integer)  # Alteração aqui
    qnt_funcionarios = db.Column(db.Integer)  # Alteração aqui
    situacao = db.Column(db.String(100))
    data = db.Column(db.String(10))

    email = db.Column(db.String(100))    
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    cep = db.Column(db.String(100))

    alunos = db.relationship('Aluno', backref='escola', lazy=True)
    
    #TESTE ALUNOS POR ESCOLA
    def count_alunos(self):
        return len(self.alunos)
    

    @staticmethod
    def count_ciclo_escola():
        return Escola.query.filter_by(categoria='CEI').count()
    

class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)
    escola = db.relationship('Escola', backref=db.backref('series', lazy=True))

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'), nullable=False)
    serie = db.relationship('Serie', backref=db.backref('turmas', lazy=True))
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)  # Adicionando a chave estrangeira para a tabela Escola
    escola = db.relationship('Escola', backref=db.backref('turmas', lazy=True))

class Periodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)
    escola = db.relationship('Escola', backref=db.backref('periodos', lazy=True))

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    genero = db.Column(db.String(100))
    ra = db.Column(db.String(100))
    cpf = db.Column(db.String(100))
    email = db.Column(db.String(100))
    data_nascimento = db.Column(db.String(10))
    responsavel1 = db.Column(db.String(100))
    responsavel2 = db.Column(db.String(100))
    aluno_nee = db.Column(db.String(100))
    auxilio = db.Column(db.String(6))
    remedio_controlado = db.Column(db.String(100))
    aluno_pcd = db.Column(db.String(6))
    aluno_reforco = db.Column(db.String(6))
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    cep = db.Column(db.String(100))
    situacao = db.Column(db.String(100))
    data_cadastro = db.Column(db.String(30))
    hora_cadastro = db.Column(db.String(30))
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    turma = db.relationship('Turma', backref=db.backref('alunos', lazy=True))
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'), nullable=False)
    serie = db.relationship('Serie', backref=db.backref('alunos', lazy=True))
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodo.id'), nullable=False)
    periodo = db.relationship('Periodo', backref=db.backref('alunos', lazy=True))

    @staticmethod
    def count_nee_students():
        return Aluno.query.filter_by(aluno_nee='Sim').count()
    
    @staticmethod
    def count_pcd_students():
        return Aluno.query.filter_by(aluno_pcd='Sim').count()
    

class Funcionarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    genero = db.Column(db.String(100))
    cpf = db.Column(db.String(100))
    email = db.Column(db.String(100))
    data_nascimento = db.Column(db.String(10))
    
    data = db.Column(db.String(10))  # Alterado para db.String
    hora = db.Column(db.String(8))  # Coluna para armazenar a hora

    matricula = db.Column(db.String(100))
    lotacao = db.Column(db.String(100))
    local_trabalho = db.Column(db.String(100))
    cargo = db.Column(db.String(100))
    efetivo = db.Column(db.String(100))
    formacao = db.Column(db.String(100))
    add1 = db.Column(db.String(100))
    add2 = db.Column(db.String(100))
    add3 = db.Column(db.String(100))

    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)
    escola = db.relationship('Escola', backref=db.backref('funcionarios', lazy=True))
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=True)
    turma = db.relationship('Turma', backref=db.backref('funcionarios', lazy=True))
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'), nullable=True)
    serie = db.relationship('Serie', backref=db.backref('funcionarios', lazy=True))
    periodo = db.Column(db.String(100))

    rua = db.Column(db.String(100))
    numero = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    cep = db.Column(db.String(100))
    situacao = db.Column(db.String(100))

    @staticmethod
    def count_agentes_funcionarios():
        return Funcionarios.query.filter_by(cargo='Agente Educacional').count()
    
    @staticmethod
    def count_professores_funcionarios():
        return Funcionarios.query.filter_by(cargo='Professor').count()


@app.route("/user/home")
def home():
    if "user_id" in session:
    
        # Consultar o total de escolas, alunos e usuários e etc.
        total_escolas = Escola.query.count()
        total_alunos = Aluno.query.count()
        total_usuarios = users.query.count()
        total_funcionarios = Funcionarios.query.count()
        total_agentes = Funcionarios.count_agentes_funcionarios()
        total_professores = Funcionarios.count_professores_funcionarios()
        total_alunos_nee = Aluno.count_nee_students()
        total_alunos_pcd = Aluno.count_pcd_students()
        total_ciclo_escola = Escola.count_ciclo_escola()

        return render_template("dashboard.html", total_escolas=total_escolas, total_alunos=total_alunos, total_usuarios=total_usuarios, total_funcionarios=total_funcionarios , total_agentes = total_agentes, total_professores = total_professores ,total_alunos_nee=total_alunos_nee, total_alunos_pcd=total_alunos_pcd, total_ciclo_escola=total_ciclo_escola, current_page='home')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/user/professores")
def professores():
    if "user_id" in session:
        # Consulta todos os professores
        professores = Funcionarios.query.filter_by(cargo="Professor").all()
        return render_template("professores.html", professores=professores, current_page='professores')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/user/alunos")
def alunos():
    # Consulta todos os alunos
    todos_alunos = Aluno.query.all()

    return render_template("alunos.html", alunos=todos_alunos, current_page='alunos')

##API USUARIOS
@app.route('/api/alunos', methods=['GET'])
def get_alunos():
    # Consulta todos os usuários
    alunos = Aluno.query.all()

    # Converte os alunos para um formato JSON
    alunos_json = [{
        'nome': aluno.nome,
        'ra': aluno.ra,
        'escola': aluno.escola.nome,
        'serie': f"{aluno.serie.nome} {aluno.turma.nome}",
        'periodo': aluno.periodo.nome,
        'status': aluno.situacao,
        'id': aluno.id
    } for aluno in alunos]

    return jsonify(alunos_json)

@app.route("/user/usuarios")
def usuarios():
     # Consulta todas os usuários
    #usuarios = users.query.all()

    return render_template("usuarios.html", usuarios=usuarios, current_page='usuarios')

##API USUARIOS
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    # Consulta todos os usuários
    usuarios = users.query.all()

    # Converte os usuários para um formato JSON
    usuarios_json = [{
        'nome': usuario.name,
        'matricula': usuario.matricula,
        'nivel': usuario.nivel_acesso,
        'cadastro': usuario.data,
        'trabalho': usuario.local_trabalho,
        'status': usuario.situacao,
        'id': usuario._id
    } for usuario in usuarios]

    return jsonify(usuarios_json)

@app.route("/user/funcionarios")
def funcionarios():
    # Consulta todas os funcionários
    funcionarios = Funcionarios.query.all()
    return render_template("funcionarios.html", funcionarios=funcionarios, current_page='funcionarios')

@app.route("/user/gestao")
def gestao():
    return render_template("gestao.html")

@app.route("/user/escolas")
def escolas():
    escolas = Escola.query.all()
    return render_template("escolas.html", escolas=escolas, current_page='escolas' )

@app.route("/user/documentos")
def documentos():
    return render_template("documentos.html", current_page='documentos' )


@app.route("/cadastro", methods=["POST", "GET"])
def cadastro():
    if "user_id" in session:
        if request.method == "POST":
            # Seu código de processamento do formulário
            nome = request.form["cd_user_nome"]
            telefone = request.form["cd_user_telefone"]
            genero = request.form["cd_user_genero"]
            cpf = request.form["cd_user_cpf"]
            email = request.form["cd_user_email"]
            data_nasc = request.form["cd_user_nascimento"]
            matricula = request.form["cd_user_matricula"]
            usuario = request.form["cd_user_usuario"]
            trabalho = request.form["cd_user_trabalho"]
            cargo = request.form["cd_user_cargo"]
            nivel_acesso = request.form["cd_user_nivel_acesso"]
            senha = request.form["cd_user_senha"]
            rua = request.form["cd_user_rua"]
            numero = request.form["cd_user_numero"]
            bairro = request.form["cd_user_bairro"]
            cidade = request.form["cd_user_municipio"]
            estado = request.form["cd_user_estado"]
            cep = request.form["cd_user_cep"]

            # Verifica se o email já está em uso
            existing_user = users.query.filter_by(email=email).first()

            if existing_user:
                flash("Email já está em uso. Por favor, escolha outro.")
            else:
                try:
                    # Obtém a data e hora atuais
                    data_atual = datetime.now().strftime('%d/%m/%Y')
                    hora_atual = datetime.now().strftime('%H:%M:%S')

                    # Crie um novo usuário com os dados fornecidos
                    usr = users(name=nome, telefone=telefone, email=email, senha=senha, data=data_atual, hora=hora_atual, genero=genero, cpf=cpf, data_nascimento=data_nasc, matricula=matricula, usuario=usuario, lotacao="Secretaria Municipal de Educação", local_trabalho=trabalho, situacao="Ativo", nivel_acesso=nivel_acesso, cargo=cargo, logradouro=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep)
                    db.session.add(usr)
                    db.session.commit()
                    flash("Cadastrado com Sucesso!", "success")
                    return redirect(url_for("usuarios"))
                except IntegrityError:
                    # Captura a exceção caso haja um problema de integridade (por exemplo, violação de chave única)
                    db.session.rollback()
                    flash("Erro ao cadastrar. Por favor, tente novamente.")
            # Redireciona para a página de cadastro após a tentativa de cadastro
            return redirect(url_for("cadastro"))
        else:
            # Se o método da requisição não for POST, apenas renderize o template de cadastro
            return render_template("cadastro.html")
    else:
        flash("Você não está conectado.")
        return redirect(url_for("login"))
    
@app.route("/cadastro_aluno", methods=["POST", "GET"])
def cadastro_aluno():
    if "user_id" in session:
        if request.method == "POST":
           # Obtém a data e hora atuais
            data_cadastro = datetime.now().strftime('%d/%m/%Y')
            hora_cadastro = datetime.now().strftime('%H:%M:%S')

            nome = request.form["cd_aluno_nome"]
            telefone = request.form["cd_aluno_telefone"]
            genero = request.form["cd_aluno_genero"]
            ra = request.form["cd_aluno_ra"]
            cpf = request.form["cd_aluno_cpf"]
            email = request.form["cd_aluno_email"]
            data_nascimento = request.form["cd_aluno_nascimento"]
            escola_id = request.form["escola"]
            # Continue capturando os outros dados do formulário...
            serie_id = request.form["serie"]  # Capturar o ID da série selecionada
            turma_id = request.form["cd_aluno_turma"]  # Capturar o ID da turma selecionada
            periodo_id = request.form["periodo"]  # Capturar o ID da turma selecionada
            
            # Exemplo:
            responsavel1 = request.form["cd_aluno_resp1"]
            responsavel2 = request.form["cd_aluno_resp2"]
            aluno_nee = request.form["cd_aluno_nee"]
            
            remedio_controlado = request.form["cd_aluno_remedio"]
            auxilio = request.form["cd_aluno_auxilio"]
            pcd = request.form["cd_aluno_pcd"]
            reforco = request.form["cd_aluno_reforco"]
            remedio_controlado = request.form["cd_aluno_remedio"]
            rua = request.form["cd_aluno_rua"]
            numero = request.form["cd_aluno_numero"]
            bairro = request.form["cd_aluno_bairro"]
            cidade = request.form["cd_aluno_municipio"]
            estado = request.form["cd_aluno_estado"]
            cep = request.form["cd_aluno_cep"]

            # Criar um novo aluno com os dados fornecidos
            novo_aluno = Aluno(nome=nome, telefone=telefone, genero=genero, ra=ra, cpf=cpf, email=email, data_nascimento=data_nascimento, responsavel1=responsavel1, responsavel2=responsavel2, aluno_nee=aluno_nee, auxilio=auxilio, remedio_controlado=remedio_controlado, aluno_pcd=pcd, aluno_reforco=reforco , rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep, situacao="Ativo", data_cadastro=data_cadastro, hora_cadastro=hora_cadastro, escola_id=escola_id)
            
            # Buscar as instâncias da turma e série com base nos IDs
            turma = Turma.query.get(turma_id)
            serie = Serie.query.get(serie_id)
            periodo = Periodo.query.get(periodo_id)

            # Busque a instância da escola
            escola = Escola.query.get(escola_id)

            # Incrementar o atributo qnt_alunos em 1
            escola.qnt_alunos += 1

            # Associar o aluno à turma e série
            novo_aluno.turma = turma
            novo_aluno.serie = serie
            novo_aluno.periodo = periodo

            # Adicionar e commitar o novo aluno ao banco de dados
            db.session.add(novo_aluno)
            db.session.commit()

            # Redirecionar para alguma página de confirmação ou outra rota
            return redirect(url_for("alunos"))

        else:
            # Se o método da requisição não for POST, apenas renderize o template de cadastro
            escolas = Escola.query.all()
            return render_template("cadastro_aluno.html", escolas=escolas)
    else:
        flash("Você não está conectado.")
        return redirect(url_for("login"))

import re

@app.route("/cadastro_escola", methods=["POST", "GET"])
def cadastro_escola():
    if "user_id" in session:
        if request.method == "POST":
            nome = request.form["cd_escola_nome"]
            telefone = request.form["cd_escola_telefone"]
            categoria = request.form["cd_escola_categoria"]
            cie = request.form["cd_escola_cie"]
            email = request.form["cd_escola_email"]
            data_criacao = request.form["cd_escola_data_criacao"]

            rua = request.form["cd_escola_rua"]
            numero = request.form["cd_escola_numero"]
            bairro = request.form["cd_escola_bairro"]
            cidade = request.form["cd_escola_municipio"]
            estado = request.form["cd_escola_estado"]
            cep = request.form["cd_escola_cep"]

            # 1. Crie uma nova entrada na tabela Escola
            nova_escola = Escola(nome=nome, telefone=telefone, categoria=categoria, tipo="", qnt_alunos=0, qnt_funcionarios=0, situacao="Ativo", codigo=cie, email=email ,data=data_criacao, rua= rua, numero = numero, bairro=bairro, cidade=cidade, estado=estado, cep = cep)
            db.session.add(nova_escola)
            db.session.commit()

            # 2. Recupere o ID da escola recém-criada
            escola_id = nova_escola.id

            # 3. Para cada checkbox selecionado no formulário, insira uma entrada na tabela Serie e Turma
            for checkbox_nome in request.form.getlist("checkboxes"):
                # Extrai a série e a turma usando expressões regulares
                match = re.match(r"(\d+° Ano) ([A-Z])", checkbox_nome)
                if match:
                    serie_nome = match.group(1)  # Obtém a série (por exemplo, "5° Ano")
                    turma_nome = match.group(2)  # Obtém a turma (por exemplo, "E")

                    # Verifica se a série já existe no banco de dados
                    serie_existente = Serie.query.filter_by(nome=serie_nome, escola_id=escola_id).first()

                    # Se a série não existir, crie uma nova série
                    if not serie_existente:
                        nova_serie = Serie(nome=serie_nome, escola_id=escola_id)
                        db.session.add(nova_serie)
                        db.session.commit()  # Salva a série no banco de dados para obter seu ID atribuído
                    else:
                        # Se a série já existir, use a série existente
                        nova_serie = serie_existente

                    # Recupera o ID da série recém-criada ou existente
                    serie_id = nova_serie.id

                    # Insira a turma no banco de dados associada à série
                    nova_turma = Turma(nome=turma_nome, serie_id=serie_id, escola_id=escola_id)
                    db.session.add(nova_turma)

            # 4. Para cada período selecionado no formulário, insira uma entrada na tabela Periodo
            periodos_selecionados = request.form.getlist("periodos")
            for periodo_nome in periodos_selecionados:
                novo_periodo = Periodo(nome=periodo_nome, escola_id=escola_id)
                db.session.add(novo_periodo)

            db.session.commit()

            return redirect(url_for("escolas"))

        else:
            # Se o método da requisição não for POST, apenas renderize o template de cadastro
            escolas = Escola.query.all()
            return render_template("cadastro_escola.html", escolas=escolas)
    else:
        flash("Você não está conectado.")
        return redirect(url_for("login"))
    

@app.route("/cadastro_professor", methods=["POST", "GET"])
def cadastro_professor():
    if "user_id" in session:
        if request.method == "POST":
            nome = request.form["cd_professor_nome"]
            telefone = request.form["cd_professor_telefone"]
            genero = request.form["cd_professor_genero"]
            cpf = request.form["cd_professor_cpf"]
            email = request.form["cd_professor_email"]
            data_nascimento = request.form["cd_professor_nascimento"]

            # Exemplo:
            matricula = request.form["cd_professor_matricula"]
            lotacao = request.form["cd_professor_lotacao"]
            cargo = request.form["cd_professor_cargo"]
            tipo = request.form["cd_professor_tipo"]
            disciplina = request.form["cd_professor_disciplina"]
            pos_graduacao = request.form["cd_professor_pos"]

            escola_id = request.form["escola"]
            # Continue capturando os outros dados do formulário...
            serie_id = request.form["serie"]  # Capturar o ID da série selecionada
            turma_id = request.form["cd_func_turma"]  # Capturar o ID da turma selecionada
            periodo = request.form["periodo"]  # Capturar o ID da turma selecionada
            
            # Exemplo:
            efetivo = request.form["cd_professor_efetivo"]
            formacao = request.form["cd_professor_formacao"]
        
            rua = request.form["cd_professor_logradouro"]
            numero = request.form["cd_professor_numero"]
            bairro = request.form["cd_professor_bairro"]
            cidade = request.form["cd_professor_municipio"]
            estado = request.form["cd_professor_estado"]
            cep = request.form["cd_professor_cep"]

            # Obtém a data e hora atuais
            data_atual = datetime.now().strftime('%d/%m/%Y')
            hora_atual = datetime.now().strftime('%H:%M:%S')

            # Criar um novo aluno com os dados fornecidos
            novo_funcionario = Funcionarios(nome=nome, telefone=telefone, genero=genero, cpf=cpf, email=email, data_nascimento=data_nascimento, data=data_atual, hora=hora_atual, matricula=matricula, lotacao=lotacao, cargo=cargo, add1=tipo, add2=disciplina, add3=pos_graduacao ,periodo=periodo, efetivo = efetivo, formacao = formacao, escola_id=escola_id, rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep, situacao="ativo")
            
            # Buscar as instâncias da turma e série com base nos IDs
            turma = Turma.query.get(turma_id)
            serie = Serie.query.get(serie_id)

            # Busque a instância da escola
            escola = Escola.query.get(escola_id)

            # Incrementar o atributo qnt_alunos em 1
            escola.qnt_funcionarios += 1

            # Associar o aluno à turma e série
            novo_funcionario.turma = turma
            novo_funcionario.serie = serie

            # Adicionar e commitar o novo aluno ao banco de dados
            db.session.add(novo_funcionario)
            db.session.commit()

            # Redirecionar para alguma página de confirmação ou outra rota
            return redirect(url_for("professores"))

        else:
            # Se o método da requisição não for POST, apenas renderize o template de cadastro
            escolas = Escola.query.all()
            return render_template("cadastro_professor.html", escolas=escolas)
    else:
        flash("Você não está conectado.")
        return redirect(url_for("login"))

@app.route("/cadastro_funcionario", methods=["POST", "GET"])
def cadastro_funcionario():
    if "user_id" in session:
        if request.method == "POST":
            nome = request.form["cd_func_nome"]
            telefone = request.form["cd_func_telefone"]
            genero = request.form["cd_func_genero"]
            cpf = request.form["cd_func_cpf"]
            email = request.form["cd_func_email"]
            data_nascimento = request.form["cd_func_nascimento"]

            # Exemplo:
            matricula = request.form["cd_func_matricula"]
            lotacao = request.form["cd_func_lotacao"]
            cargo = request.form["cd_func_cargo"]

            escola_id = request.form["escola"]
            # Continue capturando os outros dados do formulário...
            serie_id = request.form["serie"]  # Capturar o ID da série selecionada
            turma_id = request.form["cd_func_turma"]  # Capturar o ID da turma selecionada
            periodo = request.form["periodo"]  # Capturar o ID da turma selecionada
            
            # Exemplo:
            efetivo = request.form["cd_func_efetivo"]
            formacao = request.form["cd_func_formacao"]
        
            rua = request.form["cd_func_logradouro"]
            numero = request.form["cd_func_numero"]
            bairro = request.form["cd_func_bairro"]
            cidade = request.form["cd_func_municipio"]
            estado = request.form["cd_func_estado"]
            cep = request.form["cd_func_cep"]

            # Obtém a data e hora atuais
            data_atual = datetime.now().strftime('%d/%m/%Y')
            hora_atual = datetime.now().strftime('%H:%M:%S')

            # Criar um novo aluno com os dados fornecidos
            novo_funcionario = Funcionarios(nome=nome, telefone=telefone, genero=genero, cpf=cpf, email=email, data_nascimento=data_nascimento, data=data_atual, hora=hora_atual, matricula=matricula, lotacao=lotacao, cargo=cargo, add1="", add2="", add3="", periodo=periodo, efetivo = efetivo, formacao = formacao, escola_id=escola_id, rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep, situacao="ativo")
            
            # Buscar as instâncias da turma e série com base nos IDs
            turma = Turma.query.get(turma_id)
            serie = Serie.query.get(serie_id)

            # Busque a instância da escola
            escola = Escola.query.get(escola_id)

            # Incrementar o atributo qnt_alunos em 1
            escola.qnt_funcionarios += 1

            # Associar o aluno à turma e série
            novo_funcionario.turma = turma
            novo_funcionario.serie = serie

            # Adicionar e commitar o novo aluno ao banco de dados
            db.session.add(novo_funcionario)
            db.session.commit()

            # Redirecionar para alguma página de confirmação ou outra rota
            return redirect(url_for("funcionarios"))

        else:
            # Se o método da requisição não for POST, apenas renderize o template de cadastro
            escolas = Escola.query.all()
            return render_template("cadastro_funcionario.html", escolas=escolas)
    else:
        flash("Você não está conectado.")
        return redirect(url_for("login"))


@app.route("/", methods=["POST", "GET"])
def login():
    if "user_id" in session:
        flash("Você já está logado!")
        return redirect(url_for("home"))
    else:
        if request.method == "POST":
            user = request.form["nm"]
            password = request.form["senha"]
            found_user = users.query.filter_by(usuario=user).first()

            if found_user:
                # Verifica se a senha fornecida é igual à senha armazenada
                if bcrypt.checkpw(password.encode('utf-8'), found_user.senha.encode('utf-8')):
                    # Armazena o ID do usuário na sessão
                    session["user_id"] = found_user._id
                    
                    # Captura a data e hora atuais para o histórico de login
                    now = datetime.now()
                    login_entry = LoginHistory(
                        user_id=found_user._id,
                        login_date=now.strftime("%Y-%m-%d"),
                        login_time=now.strftime("%H:%M:%S")
                    )
                    
                    # Salva o login no histórico
                    db.session.add(login_entry)
                    db.session.commit()
                    
                    return redirect(url_for("home"))
                else:
                    flash("Usuário ou senha incorretos. Por favor, verifique suas credenciais.")
                    return redirect(url_for("login"))
            else:
                flash("Usuário não encontrado. Por favor, entre em contato com a TI.")
                return redirect(url_for("login"))
        else:
            return render_template("login.html")
      

@app.route("/user/perfil", methods=["GET"])
def user():
    if "user_id" in session:
        user_id = session["user_id"]

        # Recupera os dados do usuário do banco de dados
        found_user = users.query.get(user_id)

        if found_user:
            # Adiciona os dados do usuário ao contexto do template
            return render_template("user.html", user=found_user)
        else:
            flash("Usuário não encontrado!")
            return redirect(url_for("login"))
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
    
@app.route("/user/editar", methods=["POST", "GET"])
def editar():
    if "user_id" in session:
        user_id = session["user_id"]

        # Busca o usuário pelo ID
        found_user = users.query.get(user_id)

        if request.method == "POST":
            # Atualiza os dados com base no formulário
            found_user.email = request.form["email"]
            found_user.telefone = request.form["telefone"]
            found_user.genero = request.form["genero"]
            found_user.data_nascimento = request.form["edit_user_nascimento"]
            found_user.logradouro = request.form["edit_user_rua"]
            found_user.numero = request.form["edit_user_numero"]
            found_user.bairro = request.form["edit_user_bairro"]
            found_user.cidade = request.form["edit_user_cidade"]
            found_user.estado = request.form["edit_user_estado"]
            found_user.cep = request.form["edit_user_cep"]

            # Se a senha foi fornecida no formulário, atualiza o hash da senha
            senha = request.form["senha"]
            if senha:
                # Gera o hash da senha usando bcrypt
                found_user.senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Verifica o hash gerado (opcional)
                senha_valida = bcrypt.checkpw(senha.encode('utf-8'), found_user.senha.encode('utf-8'))
                print(f"Senha válida? {senha_valida}")

            # Salva as alterações no banco de dados
            db.session.commit()

            # Atualiza os valores na sessão, se necessário
            session["email"] = found_user.email
            session["telefone"] = found_user.telefone
            session["genero"] = found_user.genero
            session["data_nascimento"] = found_user.data_nascimento
            session["logradouro"] = found_user.logradouro
            session["numero"] = found_user.numero
            session["bairro"] = found_user.bairro
            session["cidade"] = found_user.cidade
            session["estado"] = found_user.estado
            session["cep"] = found_user.cep

            flash("Informações do usuário foram salvas com sucesso!")
            
            # Redireciona para a página do usuário após a edição
            return redirect(url_for("user"))

        # Se for uma requisição GET, preenche o formulário com os dados do usuário
        return render_template("editarconta.html", user=found_user)
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
@app.route("/user/alunos/aluno/editar/<int:aluno_id>", methods=["POST", "GET"])
def editar_aluno(aluno_id):
    if "user_id" in session:
        # Busca o aluno pelo ID
        found_aluno = Aluno.query.get(aluno_id)
        
        if not found_aluno:
            flash("Aluno não encontrado!")
            return redirect(url_for("user"))

        if request.method == "POST":
            # Atualiza os dados do aluno com base no formulário
            found_aluno.nome = request.form["nome"]
            found_aluno.telefone = request.form["telefone"]
            found_aluno.genero = request.form["genero"]
            found_aluno.ra = request.form["ra"]
            found_aluno.cpf = request.form["cpf"]
            found_aluno.email = request.form["email"]
            found_aluno.data_nascimento = request.form["data_nascimento"]
            found_aluno.responsavel1 = request.form["responsavel1"]
            found_aluno.responsavel2 = request.form["responsavel2"]
            found_aluno.aluno_nee = request.form["aluno_nee"]
            found_aluno.auxilio = request.form["auxilio"]
            found_aluno.remedio_controlado = request.form["remedio_controlado"]
            found_aluno.aluno_pcd = request.form["aluno_pcd"]
            found_aluno.aluno_reforco = request.form["aluno_reforco"]
            found_aluno.rua = request.form["rua"]
            found_aluno.numero = request.form["numero"]
            found_aluno.bairro = request.form["bairro"]
            found_aluno.cidade = request.form["cidade"]
            found_aluno.estado = request.form["estado"]
            found_aluno.cep = request.form["cep"]
            found_aluno.situacao = request.form["situacao"]

            # Não atualiza os campos de escola, turma, série, período, data e hora de cadastro
            # (Esses campos são omitidos da atualização)
            
            # Salva as alterações no banco de dados
            db.session.commit()

            flash("Informações do aluno foram salvas com sucesso!")
            
             # Redireciona para a página do aluno
            return redirect(url_for("mostrar_aluno", aluno_id=aluno_id))

        # Se for uma requisição GET, preenche o formulário com os dados do aluno
        return render_template("editar_aluno.html", aluno=found_aluno)
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
@app.route("/user/alunos/aluno/<int:aluno_id>", methods=["GET"])
def mostrar_aluno(aluno_id):
    if "user_id" in session:
        # Busca o aluno pelo ID
        aluno = Aluno.query.get(aluno_id)
        
        if not aluno:
            flash("Aluno não encontrado!")
            return redirect(url_for("user"))
        
        # Renderiza o template com os dados do aluno
        return render_template("mostrar_aluno.html", aluno=aluno)
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
@app.route("/user/usuarios/usuario/<int:usuario_id>", methods=["GET"])
def mostrar_usuario(usuario_id):
    if "user_id" in session:
        # Obtém o ID do usuário logado
        user_id_logado = session["user_id"]

        if user_id_logado == usuario_id:
                    # Redireciona para o próprio perfil, se não for o mesmo usuário
                    flash("Você só pode acessar o seu próprio perfil!")
                    return redirect(url_for("user"))

        # Busca o aluno pelo ID
        usuario= users.query.get(usuario_id)
        
        if not usuario:
            flash("Usuario não encontrado!")
            return redirect(url_for("user"))
        
        # Busca o último acesso do usuário na tabela LoginHistory
        ultimo_acesso = LoginHistory.query.filter_by(user_id=usuario_id).order_by(LoginHistory.login_date.desc(), LoginHistory.login_time.desc()).first()
        
        # Renderiza o template com os dados do aluno
        return render_template("mostrar_usuario.html", usuario=usuario, ultimo_acesso=ultimo_acesso)
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
@app.route("/user/usuarios/usuario/editar/<int:usuario_id>", methods=["POST", "GET"])
def editar_usuario(usuario_id):
    if "user_id" in session:
        # Busca o usuário pelo ID
        usuario = users.query.get(usuario_id)
        
        if not usuario:
            flash("Usuário não encontrado!")
            return redirect(url_for("user"))
        
        if request.method == "POST":
            # Atualiza os dados do usuário com base no formulário
            usuario.name = request.form["nome"]
            usuario.telefone = request.form["telefone"]
            usuario.genero = request.form["genero"]
            usuario.cpf = request.form["cpf"]
            usuario.email = request.form["email"]
            usuario.data_nascimento = request.form["data_nascimento"]
            usuario.matricula = request.form["matricula"]
            usuario.usuario = request.form["usuario"]
            usuario.lotacao = request.form["lotacao"]
            usuario.cargo = request.form["cargo"]
            usuario.local_trabalho = request.form["local_trabalho"]
            usuario.logradouro = request.form["logradouro"]
            usuario.numero = request.form["numero"]
            usuario.bairro = request.form["bairro"]
            usuario.cidade = request.form["cidade"]
            usuario.estado = request.form["estado"]
            usuario.cep = request.form["cep"]
            usuario.situacao = request.form["situacao"]
            usuario.nivel_acesso = request.form["nivel_acesso"]

            # Se a senha foi fornecida no formulário, atualiza o hash da senha
            senha = request.form.get("senha")
            if senha:
                # Gera o hash da senha usando bcrypt
                usuario.senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Salva as alterações no banco de dados
            db.session.commit()

            # Atualiza os valores na sessão, se necessário
            session["email"] = usuario.email
            session["telefone"] = usuario.telefone
            session["genero"] = usuario.genero
            session["data_nascimento"] = usuario.data_nascimento
            session["logradouro"] = usuario.logradouro
            session["numero"] = usuario.numero
            session["bairro"] = usuario.bairro
            session["cidade"] = usuario.cidade
            session["estado"] = usuario.estado
            session["cep"] = usuario.cep

            flash("Informações do usuário foram salvas com sucesso!")
            
            # Redireciona para a página do usuário
            return redirect(url_for("mostrar_usuario", usuario_id=usuario_id))

        # Se for uma requisição GET, preenche o formulário com os dados do usuário
        return render_template("editar_usuario.html", usuario=usuario)
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
    
@app.route("/user/logout")
def logout():
    flash("Voce saiu do sistema!")
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route('/user/alunos/gerar_pdf/<int:aluno_id>', methods=['GET'])
def gerar_pdf(aluno_id):
    if "user_id" in session:
        # Configurar o idioma para português
        #locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        # Consulta o aluno no banco de dados
        user = db.session.get(Aluno, aluno_id)

        # Verificar o período do aluno
        periodo_aluno = user.periodo.nome

        if periodo_aluno == 'Manhã':
            horario_periodo = '07:30h às 12:00h'
        elif periodo_aluno == 'Tarde':
            horario_periodo = '13:00h às 17:30h'
        else:  # Noite
            horario_periodo = '18:30h às 22:00h'

        # Converter a data de nascimento
        user.data_nascimento = datetime.strptime(user.data_nascimento, "%Y-%m-%d")

        # Formatar a data de nascimento no formato desejado
        user.data_nascimento = user.data_nascimento.strftime("%d/%m/%Y")

        # Obter a data atual
        data_atual = datetime.now().strftime("%d/%m/%Y")
        ## Obter a data atual
        #data_atual = datetime.now().strftime("%d de %B de %Y").capitalize()

        if user:
            # Renderiza o template HTML com os dados do aluno e a data atual
            html_content = render_template("declaracao.html", user=user, horario_periodo=horario_periodo, data_atual=data_atual)

            # Cria um buffer de memória
            pdf_buffer = BytesIO()

            # Cria um novo documento PDF
            doc = fitz.open()

            # Adiciona uma nova página
            page = doc.new_page()
            rect = page.rect + (36, 36, -36, -36)

            # Insere o HTML modificado na página
            page.insert_htmlbox(rect, html_content, archive=fitz.Archive("."))

            # Salva o PDF diretamente no buffer de memória
            doc.save(pdf_buffer)

            # Move o cursor para o início do buffer
            pdf_buffer.seek(0)

            # Retorna o arquivo PDF gerado sem salvá-lo no disco
            return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=False)
        else:
            return "Usuário não encontrado", 404
    else:
        return redirect(url_for("login"))
    
##verificar
##API USUARIOS
@app.route('/api/aluno/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    # Configurar o idioma para português
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    # Consulta o usuário no banco de dados
    user = db.session.get(Aluno, aluno_id)

    # Formatar a data de nascimento
    user.data_nascimento = datetime.strptime(user.data_nascimento, "%Y-%m-%d").strftime("%d/%m/%Y")
    data_atual = datetime.now().strftime("%d de %B de %Y").capitalize()

    # Converte os usuários para um formato JSON
    aluno_json = [{
        "nome": user.nome,
        "ra": user.ra,
        "data_nascimento": user.data_nascimento,
        "cidade": user.cidade,
        "estado": user.estado,
        "escola": user.escola.nome,
        "serie": user.serie.nome,
        "turma": user.turma.nome,
        "periodo": user.periodo.nome,
        "data_atual": data_atual
    }]

    response = app.response_class(
        response=json.dumps(aluno_json, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response



@app.route("/gerar_pdf_branco", methods=["GET"])
def gerar_pdf_branco():
    if "user_id" in session:
        # Renderiza o template HTML com os dados do usuário
        html_content = render_template("declaracao2.html")

        # Cria um novo documento PDF
        doc = fitz.Document()

        # Adiciona uma nova página
        page = doc.new_page()
        rect = page.rect + (36, 36, -36, -36)

        # Insere o HTML modificado na página
        page.insert_htmlbox(rect, html_content, archive=fitz.Archive("."))

        # Caminho para salvar o PDF (na pasta raiz do projeto)
        pdf_filename = f'declaracao_branco.pdf'

        # Salva o PDF
        doc.ez_save(pdf_filename)

        # Retorna o arquivo PDF gerado sem forçar download
        return send_file(pdf_filename, mimetype='application/pdf')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/gerar_pdf_conclusao_escolar", methods=["GET"])
def gerar_pdf_conclusao_escolar():
    if "user_id" in session:
        # Renderiza o template HTML com os dados do usuário
        html_content = render_template("model_declaracao_conclusao.html")

        # Cria um novo documento PDF
        doc = fitz.Document()

        # Adiciona uma nova página
        page = doc.new_page()
        rect = page.rect + (36, 36, -36, -36)

        # Insere o HTML modificado na página
        page.insert_htmlbox(rect, html_content, archive=fitz.Archive("."))

        # Caminho para salvar o PDF (na pasta raiz do projeto)
        pdf_filename = f'modelo_declaracao_conclusao_escolar.pdf'

        # Salva o PDF
        doc.ez_save(pdf_filename)

        # Retorna o arquivo PDF gerado sem forçar download
        return send_file(pdf_filename, mimetype='application/pdf')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
@app.route("/gerar_pdf_solicitacao_vaga", methods=["GET"])
def gerar_pdf_solicitacao_vaga():
    if "user_id" in session:
        # Renderiza o template HTML com os dados do usuário
        html_content = render_template("model_solicitacao_vaga.html")

        # Cria um novo documento PDF
        doc = fitz.Document()

        # Adiciona uma nova página
        page = doc.new_page()
        rect = page.rect + (36, 36, -36, -36)

        # Insere o HTML modificado na página
        page.insert_htmlbox(rect, html_content, archive=fitz.Archive("."))

        # Caminho para salvar o PDF (na pasta raiz do projeto)
        pdf_filename = f'modelo_solicitacao_vaga.pdf'

        # Salva o PDF
        doc.ez_save(pdf_filename)

        # Retorna o arquivo PDF gerado sem forçar download
        return send_file(pdf_filename, mimetype='application/pdf')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/gerar_pdf_declaracao_transferencia", methods=["GET"])
def gerar_pdf_declaracao_transferencia():
    if "user_id" in session:   
        # Renderiza o template HTML com os dados do usuário
        html_content = render_template("model_declaracao_transferencia.html")

        # Cria um novo documento PDF
        doc = fitz.Document()

        # Adiciona uma nova página
        page = doc.new_page()
        rect = page.rect + (36, 36, -36, -36)

        # Insere o HTML modificado na página
        page.insert_htmlbox(rect, html_content, archive=fitz.Archive("."))

        # Caminho para salvar o PDF (na pasta raiz do projeto)
        pdf_filename = f'modelo_declaracao_transferencia.pdf'

        # Salva o PDF
        doc.ez_save(pdf_filename)

        # Retorna o arquivo PDF gerado sem forçar download
        return send_file(pdf_filename, mimetype='application/pdf')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))


@app.route("/series/<escola_id>")
def series(escola_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        escola = Escola.query.filter_by(id=escola_id).first()
        if escola:
            series = Serie.query.filter_by(escola_id=escola_id).all()
            series_json = [{"id": serie.id, "nome": serie.nome} for serie in series]
            return jsonify(series_json)
        else:
            return jsonify([])  # Retornando uma lista vazia como resposta JSON
    else:
        return jsonify([])  # Retornando uma lista vazia se a solicitação não é AJAX


@app.route("/turmas/<serie_id>")
def turmas(serie_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Consulta as turmas da série especificada
        turmas = Turma.query.filter_by(serie_id=serie_id).all()
        if turmas:
            # Se houver turmas para a série especificada, converte para JSON e retorna
            turmas_json = [{"id": turma.id, "nome": turma.nome} for turma in turmas]
            return jsonify(turmas_json)
        else:
            # Se não houver turmas para a série especificada, retorna uma lista vazia
            return jsonify([])
    else:
        # Se a solicitação não for AJAX, retorna uma lista vazia
        return jsonify([])
    
@app.route("/periodos/<escola_id>")
def periodos(escola_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        escola = Escola.query.filter_by(id=escola_id).first()
        if escola:
            periodos = Periodo.query.filter_by(escola_id=escola_id).all()
            periodos_json = [{"id": periodo.id, "nome": periodo.nome} for periodo in periodos]
            return jsonify(periodos_json)
        else:
            return jsonify([])  # Retornando uma lista vazia como resposta JSON
    else:
        return jsonify([])  # Retornando uma lista vazia se a solicitação não é AJAX

# Executando o aplicativo com configuração para o Heroku
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    with app.app_context():
        db.create_all()  # Cria todas as tabelas do banco de dados
    app.run(host="0.0.0.0", port=port)