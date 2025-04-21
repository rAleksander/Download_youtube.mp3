import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
from pytubefix import YouTube
import os
from moviepy.editor import AudioFileClip


def atualizar_progresso(stream, chunk, bytes_restantes):
    tamanho_total = stream.filesize
    bytes_baixados = tamanho_total - bytes_restantes
    porcentagem = (bytes_baixados / tamanho_total) * 100
    progress["value"] = porcentagem
    app.update_idletasks()


def baixar_audio():
    url = entrada_url.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL do YouTube.")
        return
    
    # Seleção de pasta de salvamento
    pasta_destino = filedialog.askdirectory(title='Selecione a pasta de destino')
    if not pasta_destino:
        messagebox.showerror('Erro', 'Nenhuma pasta selecionada.')
        return
    
    try:
        # Cria uma nova instância do YouTube com callback de progresso
        yt = YouTube(url, on_progress_callback=atualizar_progresso)

        # Baixa somente o áudio
        stream = yt.streams.get_audio_only()
        output_path = stream.download(output_path=pasta_destino)

        # Verifica se o arquivo foi baixado
        if not os.path.exists(output_path):
            messagebox.showerror("Erro", "O arquivo baixado não foi encontrado.")
            return

        # Converte o arquivo .webm para .mp3
        try:
            base, ext = os.path.splitext(output_path)
            novo_arquivo = base + '.mp3'
            
            audio_clip = AudioFileClip(output_path)
            audio_clip.write_audiofile(novo_arquivo)
            audio_clip.close()
        except AttributeError as e:
            messagebox.showerror("Erro", f"Erro ao manipular o arquivo de áudio: {str(e)}")
            return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter o arquivo: {str(e)}")
            return
        finally:
            # Garante que o recurso seja liberado
            if 'audio_clip' in locals() and audio_clip is not None:
                try:
                    audio_clip.close()
                except Exception:
                    pass
    
        # Remove o vídeo e deixa somente o áudio
        os.remove(output_path)
        
        messagebox.showinfo("Sucesso", f"Download concluído: {novo_arquivo}")
        progress["value"] = 0  # Reseta a barra de progresso
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        messagebox.showerror("Erro", f"Erro ao baixar o áudio: {str(e)}")


# Criação do front-end
app = tk.Tk()
app.title("Download de Músicas do YouTube")
app.geometry("400x200")

# Texto e entrada
lbl_instrucao = tk.Label(app, text='Insira a URL da música do YouTube: ')
lbl_instrucao.pack(pady=10)

entrada_url = tk.Entry(app, width=50)
entrada_url.pack(pady=5)

# Barra de progresso
progress = Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

# Botão de download
btn_baixar = tk.Button(app, text='Baixar Áudio', command=baixar_audio)
btn_baixar.pack(pady=20)

# Inicia o app
app.mainloop()