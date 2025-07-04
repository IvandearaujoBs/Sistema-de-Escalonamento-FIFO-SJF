import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

class Processo:
    def __init__(self, nome, tempo_execucao):
        self.nome = nome
        self.tempo_execucao = tempo_execucao
        self.tempo_espera = 0
        self.turnaround = 0

def calcular_escalonamento(processos, modo):
    processos = deepcopy(processos)
    if modo == "SJF":
        processos.sort(key=lambda p: p.tempo_execucao)

    tempo_atual = 0
    for p in processos:
        p.tempo_espera = tempo_atual
        p.turnaround = p.tempo_espera + p.tempo_execucao
        tempo_atual += p.tempo_execucao

    return processos

def mostrar_resumo(processos, modo):
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, f"🔁 Algoritmo: {modo}\n")
    ordem = " → ".join(p.nome for p in processos)
    resultado_text.insert(tk.END, f"📝 Ordem de execução: {ordem}\n\n")
    for p in processos:
        resultado_text.insert(tk.END, f"🔹 {p.nome}: Espera: {p.tempo_espera}s | Execução: {p.tempo_execucao}s | Turnaround: {p.turnaround}s\n")
    media_turnaround = sum(p.turnaround for p in processos) / len(processos)
    resultado_text.insert(tk.END, f"\n🧮 Média de turnaround: {media_turnaround:.2f}s")

def adicionar_processo():
    nome = entrada_nome.get().upper()
    tempo = entrada_tempo.get()

    if not nome or not tempo:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    if nome in [p.nome for p in processos]:
        messagebox.showerror("Erro", f"O processo {nome} já foi adicionado.")
        return

    try:
        tempo = int(tempo)
        if tempo <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Tempo deve ser um número inteiro positivo.")
        return

    processos.append(Processo(nome, tempo))
    lista_processos.insert(tk.END, f"{nome} - {tempo}s")
    entrada_nome.delete(0, tk.END)
    entrada_tempo.delete(0, tk.END)

def executar_escalonamento(modo):
    if not processos:
        messagebox.showerror("Erro", "Adicione pelo menos um processo.")
        return
    resultado = calcular_escalonamento(processos, modo)
    mostrar_resumo(resultado, modo)

# Interface gráfica
janela = tk.Tk()
janela.title("Simulador de Escalonamento de Processos")
janela.geometry("600x600")

processos = []

frame_inputs = tk.Frame(janela)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Nome do Processo:").grid(row=0, column=0, padx=5)
entrada_nome = tk.Entry(frame_inputs)
entrada_nome.grid(row=0, column=1)

tk.Label(frame_inputs, text="Tempo de Execução:").grid(row=1, column=0, padx=5)
entrada_tempo = tk.Entry(frame_inputs)
entrada_tempo.grid(row=1, column=1)

btn_adicionar = tk.Button(janela, text="Adicionar Processo", command=adicionar_processo)
btn_adicionar.pack(pady=5)

lista_processos = tk.Listbox(janela, height=6)
lista_processos.pack(pady=5)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_fifo = tk.Button(frame_botoes, text="Executar FIFO", width=20, command=lambda: executar_escalonamento("FIFO"))
btn_fifo.grid(row=0, column=0, padx=10)

btn_sjf = tk.Button(frame_botoes, text="Executar SJF", width=20, command=lambda: executar_escalonamento("SJF"))
btn_sjf.grid(row=0, column=1, padx=10)

resultado_text = tk.Text(janela, height=20, width=70)
resultado_text.pack(pady=10)

janela.mainloop()
