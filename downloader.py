import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import glob
import json
import webbrowser

CONFIG_ARQUIVO = "config.json"
WGET_EXECUTAVEL = os.path.join(os.getcwd(), "wget.exe")
LISTA_DOWNLOADS = "list.txt"
PASTA_SLIDE = os.path.join(os.getcwd(), "slide")

# Função para carregar configurações do JSON
def carregar_config():
    if os.path.exists(CONFIG_ARQUIVO):
        with open(CONFIG_ARQUIVO, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

root = tk.Tk()
root.title(carregar_config().get("title", "Downloader v1.0"))
root.resizable(False, False)
root.iconbitmap("icone.ico")

# Função para centralizar a janela
def centralizar_janela(janela, largura, altura):
    janela.withdraw()
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    janela.deiconify()

centralizar_janela(root, 600, 500)

# Variáveis da interface
pasta_var = tk.StringVar()
progresso_percentual = tk.IntVar()
status_var = tk.StringVar(value="Aguardando...")

# Carregar imagens do slide
def carregar_imagens():
    imagens = glob.glob(os.path.join(PASTA_SLIDE, "*.png")) + glob.glob(os.path.join(PASTA_SLIDE, "*.jpg"))
    return imagens if imagens else None

imagens_slide = carregar_imagens()

def obter_url_slide():
    return carregar_config().get("slide_url", None)

def abrir_link_slide(event):
    url = obter_url_slide()
    if url:
        webbrowser.open(url)

slide_label = ttk.Label(root)
slide_label.pack(pady=5)
slide_label.bind("<Button-1>", abrir_link_slide)

def atualizar_slide():
    if imagens_slide:
        img_path = random.choice(imagens_slide)
        img = Image.open(img_path).resize((600, 320), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        slide_label.config(image=img_tk)
        slide_label.image = img_tk
    root.after(5000, atualizar_slide)

# Função para escolher diretório
def escolher_diretorio():
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_var.set(pasta)

def atualizar_progresso(porcentagem, mensagem="Baixando..."):
    progresso_percentual.set(porcentagem)
    status_var.set(mensagem)
    root.update_idletasks()

processos_wget = []

def iniciar_download():
    pasta = pasta_var.get()
    if not pasta:
        messagebox.showerror("Erro", "Escolha uma pasta de destino!")
        return
    if not os.path.exists(LISTA_DOWNLOADS):
        messagebox.showerror("Erro", f"O arquivo '{LISTA_DOWNLOADS}' não foi encontrado!")
        return

    def baixar():
        try:
            with open(LISTA_DOWNLOADS, "r", encoding="utf-8") as file:
                links = [linha.strip() for linha in file if linha.strip()]
            if not links:
                messagebox.showerror("Erro", "O arquivo list.txt está vazio!")
                return

            total_links = len(links)
            config = carregar_config()
            rate_limit_flag = f"--limit-rate={config.get('rate_limit', '')}".strip()

            for index, url in enumerate(links, start=1):
                nome_arquivo = os.path.basename(url)
                caminho_completo = os.path.join(pasta, nome_arquivo)
                atualizar_progresso(0, f"Iniciando {index}/{total_links}...")

                comando = f'"{WGET_EXECUTAVEL}" -c {rate_limit_flag} --progress=dot -P "{pasta}" "{url}"'.strip()
                processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                processos_wget.append(processo)

                for linha in processo.stdout:
                    if "%" in linha:
                        try:
                            porcentagem = int(linha.split("%")[0].strip().split()[-1])
                            atualizar_progresso(porcentagem, f"Baixando {index}/{total_links}... {porcentagem}%")
                        except ValueError:
                            pass
                
                processo.wait()

                if processo.returncode in [0, 8]:
                    atualizar_progresso(100, f"Download {index}/{total_links} concluído!")
                elif processo.returncode == 4:
                    atualizar_progresso(0, f"Erro 4 ao baixar {index}/{total_links}. Pulando...")
                    continue
                elif processo.returncode == 404:
                    atualizar_progresso(0, f"Arquivo não encontrado (Erro 404): {url}")
                    continue
                else:
                    messagebox.showwarning("Aviso", f"Erro ao baixar {url}. Código: {processo.returncode}")

            messagebox.showinfo("Sucesso", "Todos os downloads foram concluídos!")
            atualizar_progresso(100, "Todos os downloads finalizados!")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao baixar: {e}")

    thread = threading.Thread(target=baixar)
    thread.start()

def encerrar_processos():
    if os.path.exists("killer_app.exe"):
        try:
            subprocess.Popen("killer_app.exe", shell=True)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao executar killer_app.exe: {e}")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", encerrar_processos)

frame_pasta = ttk.Frame(root, padding=10)
frame_pasta.pack(fill="x", padx=20)

ttk.Button(frame_pasta, text="Escolher Pasta", command=escolher_diretorio).pack(side="left")
ttk.Label(frame_pasta, textvariable=pasta_var, relief="sunken", anchor="w", width=40).pack(side="left", padx=10)

progress_bar = ttk.Progressbar(root, length=500, mode="determinate", variable=progresso_percentual)
progress_bar.pack(pady=10)

ttk.Label(root, textvariable=status_var, font=("Arial", 10)).pack(pady=5)

ttk.Button(root, text="Iniciar Download", command=iniciar_download).pack(pady=10)

atualizar_slide()

root.mainloop()
