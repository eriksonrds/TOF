from ast import USub
from csv import DictReader
from tkinter import *
from tkinter.simpledialog import SimpleDialog
from turtle import bgcolor
from tkcalendar import Calendar, DateEntry
import time
from datetime import datetime
from datetime import date
import os
import shutil
from tkinter import filedialog
from tkinter import messagebox
from csv import DictReader
from dateutil.relativedelta import relativedelta
import sqlite3


def center(win):
    
    win.update_idletasks()    
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width    
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2    
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))    
    win.deiconify()   

def Tof():
    hoje = datetime.today()
    diaAtual = (hoje.day)
    mesAtual = (hoje.month)
    anoAtual = (hoje.year)
    dias = 0
    DIAS_SEM_USO = 24 * 60 * 60 * dias
    hoje1 = time.time()
    data_referencia = hoje1 - DIAS_SEM_USO
    orig = ''
    dest = ''
    ext = ''

    def selOrigem():

        with open('input\diretorios.csv', 'w', newline='') as dircsv:
            dircsv.write('origem,destino\n')
            localOrigem = filedialog.askdirectory()
            dircsv.write(f'{localOrigem}')

    def selDestino():
        with open('input\diretorios.csv', 'a', newline='') as dircsv:
            global localDestino
            localDestino = filedialog.askdirectory()
            dircsv.write(f',{localDestino}\n')         

    def arquivo_ultima_mod(arquivo):
        return os.path.getmtime(arquivo)
                
    def botaoOrigem():
        global orig
        selOrigem()
        with open('input\diretorios.csv') as diretorios:
            dados = DictReader(diretorios)
            for linha in dados:
                orig = (linha['origem'])
                
        preencherOrigem()

    def preencherOrigem():
        with open('input\diretorios.csv') as diretorios:
            dados = DictReader(diretorios)
            for linha in dados:
                localOrigem = (linha['origem'])
                texto_caminho_origem.config(text=localOrigem, anchor='w')    

    def botaoDestino():
        global dest
        selDestino()
        with open('input\diretorios.csv') as diretorios:
            dados = DictReader(diretorios)
            for linha in dados:
                dest = (linha['destino'])
        preencherDestino()

    def preencherDestino():
        with open('input\diretorios.csv') as diretorios:
            dados = DictReader(diretorios)
            for linha in dados:
                localDestino = (linha['destino'])
                texto_caminho_destino.config(text=localDestino, anchor='w')  

    def dataUltimaMod():

        def preencherDataUltimaMod():
            with open('input\periodo.csv') as periodo:
                data = DictReader(periodo)
                for linha in data:
                    data_mod = (linha['ultimaMod'])
                    campo_data_inicio.config(text=data_mod, anchor='w') 
        
        def fechar():
            cal.destroy()
            botaoAplicar.destroy()
        
        def selDataUltimaMod():
            with open('input\periodo.csv', 'w', newline='') as percsv:
                percsv.write('ultimaMod\n')
                data_mod = cal.get_date()
                percsv.write(f'{data_mod}')
        cal = Calendar(root,locale='pt_BR', date_pattern='MM/dd/yyyy', selectmode = 'day', year = anoAtual, month = mesAtual, day = diaAtual)
        cal.pack()
        cal.place(x=465, y=400, anchor="center")
        botaoAplicar = Button(root, text = "Aplicar", command = lambda: [selDataUltimaMod(), fechar(), preencherDataUltimaMod()])
        botaoAplicar.pack()
        botaoAplicar.place(x=567, y=505, anchor="center") 

    def quando_fechar():
        with open('input\periodo.csv', 'w', newline='') as percsv:
                percsv.write('')
        with open('input\diretorios.csv', 'w', newline='') as dircsv:
                dircsv.write('')        
        root.destroy()

    def verificar():
        if texto_caminho_origem.cget("text") == '':
            caixa_resposta.config(text='Por favor selecione o caminho de origem.')
        elif texto_caminho_destino.cget("text") == '':
            caixa_resposta.config(text='Por favor selecione o caminho de destino.')
        elif campo_data_inicio.cget("text") == '':
            caixa_resposta.config(text='Por favor selecione a data da ultima modificação.')         
        else:      
            global ext
            global jpg
            global pdf
            global xslx
            global dias
            with open('input\periodo.csv') as periodo:
                data = DictReader(periodo)
                for linha in data:
                    data_mod = (linha['ultimaMod'])
                    data_mod_new = datetime.strptime(data_mod, '%d/%m/%Y')
                    difereca_dias = abs((hoje - data_mod_new).days)
                    dias = difereca_dias


            if jpg.get() == 1 and pdf.get() == 0 and xslx.get() == 0:
                ext = '.jpeg'
                contagem_arquivos = 0
                for diretorio, subpastas, arquivos in os.walk(orig):
                    for arquivo in arquivos:
                        if arquivo.endswith(ext):
                            orig_arquivo = os.path.join(diretorio, arquivo)
                            if os.path.isfile(orig_arquivo) and arquivo_ultima_mod(orig_arquivo) < data_referencia:
                                contagem_arquivos += 1
                caixa_resposta.config(text=('Foram encontrados '+ str(contagem_arquivos) +' arquivos '+ str(ext) + " a mais de " + str(dias) + " dias sem uso."))
            
            elif jpg.get() == 0 and pdf.get() == 1 and xslx.get() == 0:
                ext = '.pdf'
                contagem_arquivos = 0
                for diretorio, subpastas, arquivos in os.walk(orig):
                    for arquivo in arquivos:
                        if arquivo.endswith(ext):
                            orig_arquivo = os.path.join(orig, arquivo)
                            if os.path.isfile(orig_arquivo) and arquivo_ultima_mod(orig_arquivo) < data_referencia:
                                contagem_arquivos += 1
                caixa_resposta.config(text=('Foram encontrados '+ str(contagem_arquivos) +' arquivos '+ str(ext) + " a mais de " + str(dias) + " dias sem uso.")) 
            
            elif jpg.get() == 0 and pdf.get() == 0 and xslx.get() == 1:
                ext = '.xslx'
                contagem_arquivos = 0
                for diretorio, subpastas, arquivos in os.walk(orig):
                    for arquivo in arquivos:
                        if arquivo.endswith(ext):
                            orig_arquivo = os.path.join(orig, arquivo)
                            if os.path.isfile(orig_arquivo) and arquivo_ultima_mod(orig_arquivo) < data_referencia:
                                contagem_arquivos += 1
                caixa_resposta.config(text=('Foram encontrados '+ str(contagem_arquivos) +' arquivos '+ str(ext) + " a mais de " + str(dias) + " dias sem uso.")) 

            elif jpg.get() == 0 and pdf.get() == 0 and xslx.get() == 0:
                caixa_resposta.config(text='Por favor selecione uma extesão.')              
            
            else:
                caixa_resposta.config(text='Por favor selecione somente uma extesão.')   

    def data_ultima_mod(arquivo):
        return os.path.getmtime(arquivo)

    def mover():
        aviso = messagebox.askyesno('Mover arquivos', 'Tem certeza que gostaria de mover os arquivos selecionados?')
        if aviso == YES:
            for diretorio, subpastas, arquivos in os.walk(orig):
                for arquivo in arquivos:             
                    if arquivo.endswith(ext):
                            orig_arquivo = os.path.join(diretorio, arquivo)
                            print(orig_arquivo)
                            if os.path.isfile(orig_arquivo) and arquivo_ultima_mod(orig_arquivo) < data_referencia:
                                    dest_arquivo = os.path.join(dest, arquivo)
                                    shutil.move(orig_arquivo, dest_arquivo)                                                     
            caixa_resposta.config(text=("Os arquivos foram movidos para pasta de destino.")) 

    def copiar():
        aviso = messagebox.askyesno('Mover arquivos', 'Tem certeza que gostaria de mover os arquivos selecionados?')
        if aviso == YES:
            for diretorio, subpastas, arquivos in os.walk(orig):
                for arquivo in arquivos: 
                    if arquivo.endswith(ext):
                            orig_arquivo = os.path.join(diretorio, arquivo)
                            if os.path.isfile(orig_arquivo) and arquivo_ultima_mod(orig_arquivo) < data_referencia:
                                    dest_arquivo = os.path.join(dest, arquivo)
                                    shutil.copy(orig_arquivo, dest_arquivo)                                                     
            caixa_resposta.config(text=("Os arquivos foram movidos para pasta de destino.")) 

    def sobre():
        messagebox.showinfo("sobre",'''TOF - Transfer Old Files\nVersão 1.0
        \nDesenvolvido por Eritech - IT Solutions\nE-mail: eritechitsolutions@gmail.com\nTelefone: (41) 99750-9514''')              


    def telaCadastro():

        def cadastrarUsuario():
            nome = caixa_nome.get()
            login = caixa_login.get()
            senha = caixa_senha.get()
            c_senha = caixa_confirm_senha.get()

            if (senha == c_senha):
                try:
                    banco = sqlite3.connect('tof.db')
                    cursor = banco.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (nome text,login text,senha text)")
                    cursor.execute("INSERT INTO usuarios VALUES ('"+nome+"','"+login+"','"+senha+"')")

                    banco.commit()
                    banco.close()
                except sqlite3.Error as erro:
                    print("Erro ao inserir os dados: ", erro)
            else:
                messagebox.showinfo('erro', 'As senhas digitadas são diferentes')       
        
        telaCadastro = Tk()
        telaCadastro.title("Cadastro de usuários")
        telaCadastro.geometry("250x400")
        telaCadastro.configure(bg="gainsboro")
        telaCadastro.resizable(False, False)

        texto_nome = Label(telaCadastro, text= 'Nome do usuário', font=('Helvetica', 10))
        texto_nome.place(x=20, y=40)
        texto_nome.configure(bg='gainsboro')
        caixa_nome=Entry(telaCadastro, width=35)
        caixa_nome.place(x=125, y=70, anchor="center")

        texto_login = Label(telaCadastro, text= 'Login', font=('Helvetica', 10))
        texto_login.place(x=20, y=90)
        texto_login.configure(bg='gainsboro')
        caixa_login=Entry(telaCadastro, width=35)
        caixa_login.place(x=125, y=120, anchor="center")

        texto_senha = Label(telaCadastro, text= 'Senha', font=('Helvetica', 10))
        texto_senha.place(x=20, y=140)
        texto_senha.configure(bg='gainsboro')
        caixa_senha=Entry(telaCadastro, show="*", width=35)
        caixa_senha.place(x=125, y=170, anchor="center")

        texto_confirm_senha = Label(telaCadastro, text= 'Confirmar senha', font=('Helvetica', 10))
        texto_confirm_senha.place(x=20, y=190)
        texto_confirm_senha.configure(bg='gainsboro')
        caixa_confirm_senha=Entry(telaCadastro, show="*", width=35)
        caixa_confirm_senha.place(x=125, y=220, anchor="center")

        botao_cadastrar = Button(telaCadastro, text= 'Cadastrar', bg='gainsboro', command=cadastrarUsuario)
        botao_cadastrar.place(x=125, y=270, anchor="center")

        center(telaCadastro)


    def telaConfig():
                   
        telaConfig = Tk()
        telaConfig.title("Configurações")
        telaConfig.geometry("400x400")
        telaConfig.configure(bg="gainsboro")
        telaConfig.resizable(False, False)
               
        center(telaConfig)

    def telaAlterarSenha():

        def alterarSenha():
            login = caixa_login.get()
            senha_atual = caixa_senha_atual.get()
            nova_senha = caixa_nova_senha.get()
            c_senha = caixa_confirm_senha.get()
            banco = sqlite3.connect('tof.db')
            cursor = banco.cursor()

            try:
                cursor.execute("SELECT senha FROM usuarios WHERE login = '{}'".format(login))
                senha_bd = cursor.fetchall()
                banco.close

                if senha_atual == senha_bd[0][0]:
            
                    if (nova_senha == c_senha):
                        try:
                            banco = sqlite3.connect('tof.db')
                            cursor = banco.cursor()
                            cursor.execute("UPDATE usuarios SET senha = "+nova_senha+" WHERE login='{}'".format(login))
                            
                            banco.commit()
                            banco.close()
                        except sqlite3.Error as erro:
                            messagebox.showinfo('Erro ao alterar senha', erro)
                    else:
                        messagebox.showinfo('Erro ao alterar senha', 'As senhas digitadas são diferentes')
                else:
                    messagebox.showinfo('Erro ao alterar senha', 'Senha atual incorreta!')
            except:
                messagebox.showinfo('Erro ao alterar senha','Usuário não encontrado!')


            
        telaAlterarSenha = Tk()
        telaAlterarSenha.title("Alterar Senha")
        telaAlterarSenha.geometry("200x300")
        telaAlterarSenha.configure(bg="gainsboro")
        telaAlterarSenha.resizable(False, False)

        texto_alterarSenha = Label(telaAlterarSenha, text= 'Alterar Senha', font=('Helvetica', 10))
        texto_alterarSenha.place(x=20, y=20)
        texto_alterarSenha.configure(bg='gainsboro')

        texto_login = Label(telaAlterarSenha, text= 'Login', font=('Helvetica', 10))
        texto_login.place(x=20, y=50)
        texto_login.configure(bg='gainsboro')
        caixa_login=Entry(telaAlterarSenha, width=25)
        caixa_login.place(x=20, y=70, )

        texto_senha_atual = Label(telaAlterarSenha, text= 'Senha atual', font=('Helvetica', 10))
        texto_senha_atual.place(x=20, y=90)
        texto_senha_atual.configure(bg='gainsboro')
        caixa_senha_atual=Entry(telaAlterarSenha, show="*", width=25)
        caixa_senha_atual.place(x=20, y=110)

        texto_nova_senha = Label(telaAlterarSenha, text= 'Nova senha', font=('Helvetica', 10))
        texto_nova_senha.place(x=20, y=130)
        texto_nova_senha.configure(bg='gainsboro')
        caixa_nova_senha=Entry(telaAlterarSenha, show="*", width=25)
        caixa_nova_senha.place(x=20, y=150)

        texto_confirm_senha = Label(telaAlterarSenha, text= 'Confirmar senha', font=('Helvetica', 10))
        texto_confirm_senha.place(x=20, y=170)
        texto_confirm_senha.configure(bg='gainsboro')
        caixa_confirm_senha=Entry(telaAlterarSenha, show="*", width=25)
        caixa_confirm_senha.place(x=20, y=190)

        botao_alterarSenha = Button(telaAlterarSenha, text= 'Alterar Senha', bg='gainsboro', command=alterarSenha)
        botao_alterarSenha.place(x=60, y=220)
        
        center(telaAlterarSenha)

    root = Tk()
    root.attributes('-alpha', 0.0)
    root.title("TOF - Tranfer Old Files")
    root.geometry("600x600")
    root.configure(bg="gainsboro")
    root.resizable(False, False)

    barra_menu = Menu(root, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
    Arquivo = Menu(barra_menu, tearoff=0, background='white', foreground='black')  
    Arquivo.add_command(label="Cadastrar Usuário", command=telaCadastro)
    Arquivo.add_command(label="Alterar Senha", command=telaAlterarSenha)   
    Arquivo.add_command(label="Configurações", command=telaConfig) 
    barra_menu.add_cascade(label="Arquivo", menu=Arquivo)
    Ajuda = Menu(barra_menu, tearoff=0, background='white', foreground='black')  
    Ajuda.add_command(label="Sobre", command=sobre)  
    barra_menu.add_cascade(label="Ajuda", menu=Ajuda)
    

    rodape = Label(root, text= 'Versão 1.1.0', font=('Helvetica', 8), relief='ridge', anchor='e')
    rodape.config(width=99, height=1)
    rodape.place(x=300, y=589, anchor="center")
    rodape.configure(bg="gainsboro", fg='gray')

    botaoSelecionar = PhotoImage(file = 'C:/Users/bmt003/Desktop/TransFile/img/botaoSelecionar.png')
    botaoVerificar = PhotoImage(file = 'C:/Users/bmt003/Desktop/TransFile/img/botaoVerificar.png')
    botaoMover = PhotoImage(file = 'C:/Users/bmt003/Desktop/TransFile/img/botaoMover.png')
    botaoCopiar = PhotoImage(file = 'C:/Users/bmt003/Desktop/TransFile/img/botaoCopiar.png')


    texto_local_origem = Label(root, text= 'Local de Origem', font=('Helvetica', 10))
    texto_local_origem.place(x=95, y=170, anchor="center")
    texto_local_origem.configure(bg='gainsboro')

    texto_caminho_origem = Label(root, text='', relief='sunken')
    texto_caminho_origem.config(width=40)
    texto_caminho_origem.place(x=295, y=170, anchor="center")
    texto_caminho_origem.configure(bg="white")

    botao_origem = Button(root,image = botaoSelecionar, bg='gainsboro', relief='flat',command=botaoOrigem)
    botao_origem.place(x=490, y=170, anchor="center")

    texto_local_destino = Label(root, text= 'Local de Destino', font=('Helvetica', 10))
    texto_local_destino.place(x=95, y=210, anchor="center")
    texto_local_destino.configure(bg='gainsboro')

    texto_caminho_destino = Label(root, text='', relief='sunken')
    texto_caminho_destino.config(width=40)
    texto_caminho_destino.place(x=295, y=210, anchor="center")
    texto_caminho_destino.configure(bg="white")

    botao_destino = Button(root, image = botaoSelecionar, bg='gainsboro', relief='flat', command=botaoDestino)
    botao_destino.place(x=490, y=210, anchor="center")

    jpg = IntVar()
    pdf = IntVar()
    xslx = IntVar()

    checkbox_jpg = Checkbutton(root, text= "JPG", variable=jpg, onvalue=1, offvalue=0)
    checkbox_jpg.place(x=200, y=250, anchor="center")
    checkbox_jpg.configure(bg='gainsboro')

    checkbox_pdf = Checkbutton(root, text= "PDF", variable=pdf, onvalue=1, offvalue=0)
    checkbox_pdf.place(x=250, y=250, anchor="center")
    checkbox_pdf.configure(bg='gainsboro')

    checkbox_xlsx = Checkbutton(root, text= "XSLX", variable=xslx, onvalue=1, offvalue=0)
    checkbox_xlsx.place(x=300, y=250, anchor="center")
    checkbox_xlsx.configure(bg='gainsboro')    

    texto_data_inicio = Label(root, text= 'Data da ultima modificação', font=('Helvetica', 10))
    texto_data_inicio.place(x=185, y=300, anchor="center")
    texto_data_inicio.configure(bg='gainsboro')

    campo_data_inicio = Label(root, text='', relief='sunken')
    campo_data_inicio.config(width=10)
    campo_data_inicio.place(x=320, y=300, anchor="center")
    campo_data_inicio.configure(bg="white")

    botao_data_inicio = Button(root, image = botaoSelecionar, bg='gainsboro', relief='flat',command= dataUltimaMod)
    botao_data_inicio.place(x=405, y=300, anchor="center")

    botao_verificar = Button(root, image = botaoVerificar, bg='gainsboro', relief='flat', command=verificar)
    botao_verificar.place(x=300, y=350, anchor="center")

    caixa_resposta = Label(root, text= '', font=('Helvetica', 10), relief='sunken', anchor='nw')
    caixa_resposta.config(width=50, height=5)
    caixa_resposta.place(x=300, y=440, anchor="center")
    caixa_resposta.configure(bg='white')

    botao_copiar = Button(root, image = botaoCopiar, bg='gainsboro', relief='flat', command=copiar)
    botao_copiar.place(x=200, y=530, anchor="center")

    botao_mover = Button(root, image = botaoMover, bg='gainsboro', relief='flat', command=mover)
    botao_mover.place(x=400, y=530, anchor="center")

    camada_logo = Canvas(root, bg='gainsboro', height=150, width=300, highlightthickness=0)
    camada_logo.pack
    camada_logo.place(x=300, y=80, anchor="center")
    logotk = PhotoImage(file = 'C:/Users/bmt003/Desktop/TransFile/img/logo.png')
    image = camada_logo.create_image(150, 75, anchor="center", image=logotk)

    center(root)

    root.attributes('-alpha', 1.0)

    root.iconbitmap('C:/Users/bmt003/Desktop/TransFile/img/TOF.ico')
    root.config(menu=barra_menu)
    root.protocol("WM_DELETE_WINDOW", quando_fechar)
    root.mainloop()

def entrar_TOF(event):
        
        login = caixa_login.get()
        senha = caixa_senha.get()
        banco = sqlite3.connect('tof.db')
        cursor = banco.cursor()
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE login = '{}'".format(login))
            senha_bd = cursor.fetchall()
            banco.close

            if senha == senha_bd[0][0]:
                telaLogin.destroy()
                Tof()
                
            else:
                caixa_retorno.config(text=("Senha incorreta!")) 
                
        except:
            caixa_retorno.config(text=("Usuário não encontrado!"))

def entrar_TOF_clique():
        
        login = caixa_login.get()
        senha = caixa_senha.get()
        banco = sqlite3.connect('tof.db')
        cursor = banco.cursor()
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE login = '{}'".format(login))
            senha_bd = cursor.fetchall()
            banco.close

            if senha == senha_bd[0][0]:
                telaLogin.destroy()
                Tof()
                
            else:
                caixa_retorno.config(text=("Senha incorreta!"))                 
        except:
            caixa_retorno.config(text=("Usuário não encontrado!"))              
   
telaLogin = Tk()
telaLogin.attributes('-alpha', 0.0)
telaLogin.title("Login")
telaLogin.geometry("200x220")
telaLogin.configure(bg="gainsboro")
telaLogin.resizable(False, False)

texto_login = Label(telaLogin, text= 'Login', font=('Helvetica', 10))
texto_login.place(x=100, y=50, anchor='center')
texto_login.configure(bg='gainsboro')
caixa_login=Entry(telaLogin, width=20)
caixa_login.place(x=100, y=70, anchor="center")

texto_senha = Label(telaLogin, text= 'Senha', font=('Helvetica', 10))
texto_senha.place(x=100, y=100, anchor='center')
texto_senha.configure(bg='gainsboro')
caixa_senha=Entry(telaLogin, show="*", width=20)
caixa_senha.place(x=100, y=120, anchor="center")

botao_entrar = Button(telaLogin, text= 'Entrar', bg='gainsboro', command=entrar_TOF_clique)
botao_entrar.place(x=100, y=160, anchor="center")

caixa_retorno = Label(telaLogin, text= '', font=('Helvetica', 10), relief='flat', anchor='center')
caixa_retorno.config(width=20, height=1)
caixa_retorno.place(x=100, y=190, anchor="center")
caixa_retorno.configure(bg='gainsboro')
center(telaLogin)

telaLogin.bind('<Return>', entrar_TOF)

telaLogin.attributes('-alpha', 1.0)
telaLogin.iconbitmap('C:/Users/bmt003/Desktop/TransFile/img/TOF.ico')
telaLogin.mainloop()


