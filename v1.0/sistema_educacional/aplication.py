from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'db1.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime=timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    telefone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    data = db.Column(db.String(10))  # Alterado para db.String
    hora = db.Column(db.String(8))  # Coluna para armazenar a hora

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
    
    def __init__(self, name, telefone, email, senha, data, hora, genero, cpf, data_nascimento, matricula, usuario, lotacao, cargo, local_trabalho, logradouro, numero, bairro, cidade, estado, cep):
        self.name = name
        self.telefone = telefone
        self.email = email
        self.senha = generate_password_hash(senha)  # Gera e armazena o hash da senha
        self.data = data
        self.hora = hora

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
    alunos = db.relationship('Aluno', backref='escola', lazy=True)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    escola_id = db.Column(db.Integer, db.ForeignKey('escola.id'), nullable=False)

@app.route("/user/home")
def home():
    if "user" in session:
        user = session["user"]
        return render_template("dashboard.html", current_page='home')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/user/professores")
def view():
    if "user" in session:
        user = session["user"]
        return render_template("view.html", values=users.query.all(), current_page='view')
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))

@app.route("/user/alunos")
def alunos():
     # Consulta todas as escolas
    todas_escolas = Escola.query.all()
    # Cria um dicionário para armazenar os alunos por escola
    alunos_por_escola = {}

    # Itera sobre todas as escolas
    for escola in todas_escolas:
        # Consulta os alunos associados a cada escola
        alunos_da_escola = Aluno.query.filter_by(escola_id=escola.id).all()
        # Armazena os alunos no dicionário usando o nome da escola como chave
        alunos_por_escola[escola.nome] = alunos_da_escola

    return render_template("alunos.html", alunos_por_escola=alunos_por_escola, current_page='alunos')

@app.route("/user/usuarios")
def usuarios():
     # Consulta todas as escolas
    usuarios = users.query.all()


    return render_template("usuarios.html", usuarios=usuarios, current_page='usuarios')

@app.route("/gestao")
def gestao():
    escolas = Escola.query.all()
    return render_template("gestao.html", escolas=escolas, current_page='gestao')

@app.route("/escolas")
def escolas():
    escolas = Escola.query.all()
    return render_template("escolas.html", escolas=escolas, current_page='escolas' )

@app.route("/contato")
def contato():
    return render_template("contato.html")



@app.route("/cadastro", methods=["POST", "GET"])
def cadastro():
    if "user" in session:
        
        if request.method == "POST":
            user = request.form["cd_user_nome"]
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
                # Tenta adicionar o novo usuário ao banco de dados
                try:

                    # Obtém a data e hora atuais
                    data_atual = datetime.now().strftime('%d/%m/%Y')
                    hora_atual = datetime.now().strftime('%H:%M:%S')

                    usr = users(name=user, telefone=telefone, email=email, senha=senha, data=data_atual, hora=hora_atual, genero=genero, cpf=cpf, data_nascimento=data_nasc, matricula=matricula, usuario=usuario, lotacao="Secretaria Municipal de Educação", local_trabalho=trabalho, cargo=cargo, logradouro=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep)
                    db.session.add(usr)
                    db.session.commit()
                    flash("Cadastrado com Sucesso!")
                    session["user"] = user
                    session["email"] = email  # Corrigir aqui
                    return redirect(url_for("user"))
                except IntegrityError:
                    # Captura a exceção caso haja um problema de integridade (por exemplo, violação de chave única)
                    db.session.rollback()
                    flash("Erro ao cadastrar. Por favor, tente novamente.")
                    return redirect(url_for("cadastro"))  # Adiciona um redirecionamento para a página de cadastro

        else:
            # Se o método da requisição não for POST, apenas renderize o template de cadastro
            return render_template("cadastro.html")
    else:
        flash("Você não está conectado.")
        return redirect(url_for("login"))


@app.route("/", methods=["POST", "GET"])
def login():
    if "user" in session:
            user = session["user"]
            flash("Você já está logado!")
            return redirect(url_for("user"))
    else:
        #SE REALIZADO TENTATIVA DE LOGIN
        if request.method == "POST":
            user = request.form["nm"]
            password = request.form["senha"]
            #CONSULTA USUARIO NO BD
            found_user = users.query.filter_by(name=user).first()
            #SE EXISTE O USUÁRIO
            if found_user:
                #SE O USUARIO E SENHA BATE
                if found_user and check_password_hash(found_user.senha, password):
                    session["user"] = user
                    session["email"] = found_user.email
                    session.permanent = True
                    flash("Login com Sucesso!")
                    return redirect(url_for("user"))
                #TENTE ACESSAR NOVAMENTE COM A SENHA
                else:
                    flash("Usuário ou senha incorretos. Por favor, verifique suas credenciais.")
                    return redirect(url_for("login"))
            # O USUARIO NAO EXISTE
            else:
                flash("Usuário não encontrado. Por favor, registre-se primeiro.")
                return redirect(url_for("cadastro"))
        #SE JA ESTA LOGADO
        else:
            if "user" in session:
                flash("Você já está logado!")
                return redirect(url_for("user"))

            else:
                return render_template("login.html")

@app.route("/user", methods=["GET"])
def user():
    if "user" in session:
        user = session["user"]

        # Recupera os dados do usuário do banco de dados
        found_user = users.query.filter_by(name=user).first()

        if found_user:
            # Adiciona os dados do usuário ao contexto do template
            return render_template("user.html", user=found_user)
        else:
            flash("Usuário não encontrado!")
            return redirect(url_for("login"))
    else:
        flash("Você não está logado!")
        return redirect(url_for("login"))
    
    
@app.route("/editar", methods=["POST", "GET"])
def editar():
    if "user" in session:
        user = session["user"]

        # Busca o usuário pelo nome
        found_user = users.query.filter_by(name=user).first()

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
    
@app.route("/logout")
def logout():
    
    flash("Voce saiu do sistema!")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
       db.create_all()
    app.run(debug=True)