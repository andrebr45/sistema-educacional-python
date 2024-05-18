from flask import Flask, redirect, url_for, render_template, request, session, flash, send_file, abort, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import fitz
import locale

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
    senha = db.Column(db.String(100))
    data = db.Column(db.String(10))  # Alterado para db.String
    hora = db.Column(db.String(8))  # Coluna para armazenar a hora
    situacao = db.Column(db.String(8))

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
    
    def __init__(self, name, telefone, email, senha, data, hora, genero, cpf, data_nascimento, matricula, usuario, lotacao, cargo, local_trabalho, situacao, logradouro, numero, bairro, cidade, estado, cep):
        self.name = name
        self.telefone = telefone
        self.email = email
        self.senha = generate_password_hash(senha)  # Gera e armazena o hash da senha
        self.data = data
        self.hora = hora
        self.situacao = situacao

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

    
    def set_senha(self, senha):
            self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
            return check_password_hash(self.senha_hash, senha)

class Escola(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    codigo = db.Column(db.String(100))
    ciclo = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    qnt_alunos = db.Column(db.Integer)  # Alteração aqui
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
        return Escola.query.filter_by(ciclo='I').count()
    

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

@app.route("/user/usuarios")
def usuarios():
     # Consulta todas os usuários
    usuarios = users.query.all()

    return render_template("usuarios.html", usuarios=usuarios, current_page='usuarios')

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
                    usr = users(name=nome, telefone=telefone, email=email, senha=senha, data=data_atual, hora=hora_atual, genero=genero, cpf=cpf, data_nascimento=data_nasc, matricula=matricula, usuario=usuario, lotacao="Secretaria Municipal de Educação", local_trabalho=trabalho, situacao="Ativo", cargo=cargo, logradouro=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep)
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
            novo_aluno = Aluno(nome=nome, telefone=telefone, genero=genero, ra=ra, cpf=cpf, email=email, data_nascimento=data_nascimento, responsavel1=responsavel1, responsavel2=responsavel2, aluno_nee=aluno_nee, auxilio=auxilio, remedio_controlado=remedio_controlado, aluno_pcd=pcd, aluno_reforco=reforco , rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep, situacao="ativo", escola_id=escola_id)
            
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
            ciclo = request.form["cd_escola_ciclo"]
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
            nova_escola = Escola(nome=nome, telefone=telefone, ciclo=ciclo, qnt_alunos=0, situacao="Ativo", codigo=cie, email=email ,data=data_criacao, rua= rua, numero = numero, bairro=bairro, cidade=cidade, estado=estado, cep = cep)
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
            escola.qnt_alunos += 1

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
            escola.qnt_alunos += 1

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
                if check_password_hash(found_user.senha, password):
                    session["user_id"] = found_user._id
                    return redirect(url_for("home"))
                else:
                    flash("Usuário ou senha incorretos. Por favor, verifique suas credenciais.")
                    return redirect(url_for("login"))
            else:
                flash("Usuário não encontrado. Por favor, Entre em contato com a TI.")
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
            found_user.cidade= request.form["edit_user_cidade"]
            found_user.estado= request.form["edit_user_estado"]
            found_user.cep = request.form["edit_user_cep"]
            
            # Se a senha foi fornecida no formulário, atualiza o hash da senha
            senha = request.form["senha"]
            if senha:
                found_user.senha = generate_password_hash(senha)
            
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
    
@app.route("/user/logout")
def logout():
    flash("Voce saiu do sistema!")
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/gerar_pdf/<int:aluno_id>", methods=["GET"])
def gerar_pdf(aluno_id):
    if "user_id" in session:
        # Configurar o idioma para português
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        # Consulta o usuário no banco de dados
        user = db.session.query(Aluno).get(aluno_id)

        # Verificar o período do aluno
        periodo_aluno = user.periodo.nome

        if periodo_aluno == 'Manhã':
            horario_periodo = '07:30h às 12:00h'
        elif periodo_aluno == 'Tarde':
            horario_periodo = '13:00h às 17:30h'
        else:  # Noite
            horario_periodo = '18:30h às 22:00h'
        
        user.data_nascimento = datetime.strptime(user.data_nascimento, "%Y-%m-%d")

        # Formatar a data de nascimento no formato desejado
        user.data_nascimento = user.data_nascimento.strftime("%d/%m/%Y")

        # Obter a data atual
        data_atual = datetime.now().strftime("%d de %B de %Y").capitalize()

        if user:
            # Renderiza o template HTML com os dados do usuário
            html_content = render_template("declaracao.html", user=user, data_atual=data_atual, horario_periodo=horario_periodo)

            # Cria um novo documento PDF
            doc = fitz.Document()

            # Adiciona uma nova página
            page = doc.new_page()
            rect = page.rect + (36, 36, -36, -36)

            # Insere o HTML modificado na página
            page.insert_htmlbox(rect, html_content, archive=fitz.Archive("."))

            # Caminho para salvar o PDF (na pasta raiz do projeto)
            pdf_filename = f'declaracao_{aluno_id}.pdf'

            # Salva o PDF
            doc.ez_save(pdf_filename)

            # Retorna o arquivo PDF gerado sem download
            return send_file(pdf_filename, mimetype='application/pdf')
        else:
            return "Usuário não encontrado"
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

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

if __name__ == "__main__":
    with app.app_context():
       db.create_all()
    app.run(debug=True)