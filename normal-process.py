import time
from rich.console import Console
from rich.progress import Progress
from copy import deepcopy

console = Console()

class Processo:
    def __init__(self, nome, tempo_execucao):
        self.nome = nome
        self.tempo_execucao = tempo_execucao
        self.tempo_espera = 0
        self.turnaround = 0

    def executar(self, tempo_atual, velocidade=0.2):
        self.tempo_espera = tempo_atual
        self.turnaround = self.tempo_espera + self.tempo_execucao

        console.print(f"\n🔄 [bold]{self.nome}[/bold]")
        console.print(f"Tempo de espera: [yellow]{self.tempo_espera}[/yellow]s")
        console.print(f"Tempo de execução: [cyan]{self.tempo_execucao}[/cyan]s")
        console.print(f"Turnaround: [magenta]{self.turnaround}[/magenta]s")

        with Progress() as progress:
            task_id = progress.add_task(f"[green]{self.nome}[/green]", total=self.tempo_execucao)
            for _ in range(self.tempo_execucao):
                time.sleep(velocidade)
                progress.update(task_id, advance=1)

        console.print(f"✅ [bold]{self.nome}[/bold] finalizado!")

def obter_processos():
    processos = []
    n = int(input("Quantos processos deseja adicionar? "))
    nomes_usados = set()

    for i in range(n):
        while True:
            nome = input(f"Digite o nome do {i+1}º processo (ex: A, B, C...): ").upper()
            if nome and nome not in nomes_usados:
                nomes_usados.add(nome)
                break
            else:
                console.print("[red]Nome inválido ou já usado. Tente outro.[/red]")
        tempo = int(input(f"Digite o tempo de execução do processo {nome}: "))
        processos.append(Processo(nome, tempo))

    return processos

def executar_processos(processos):
    tempo_atual = 0
    for processo in processos:
        processo.executar(tempo_atual)
        tempo_atual += processo.tempo_execucao

def mostrar_resumo(processos):
    console.print("\n📊 [bold]Resumo Final:[/bold]")
    for p in processos:
        console.print(f"🔹 {p.nome} → Espera: {p.tempo_espera}s | Execução: {p.tempo_execucao}s | Turnaround: {p.turnaround}s")
    media_turnaround = sum(p.turnaround for p in processos) / len(processos)
    console.print(f"🧮 [bold]Média de turnaround: [/bold] [blue]{media_turnaround:.2f}[/blue]s")

    ordem = " → ".join([p.nome for p in processos])
    console.print(f"\n📝 [bold]Ordem final de execução dos processos:[/bold] [green]{ordem}[/green]")

def simular_escalonamento(tipo, processos_originais):
    # Faz uma cópia dos processos para não perder dados
    processos = deepcopy(processos_originais)

    if tipo == '1':
        console.print("\n▶️ [bold]Executando com FIFO[/bold]")
        processos_ordenados = processos
    elif tipo == '2':
        console.print("\n▶️ [bold]Executando com SJF[/bold]")
        processos_ordenados = sorted(processos, key=lambda p: p.tempo_execucao)
    else:
        console.print("[red]Tipo de escalonamento inválido[/red]")
        return

    ordem = " → ".join([p.nome for p in processos_ordenados])
    console.print(f"\n📝 [bold]Ordem de execução dos processos:[/bold] [green]{ordem}[/green]\n")

    executar_processos(processos_ordenados)
    mostrar_resumo(processos_ordenados)

def main():
    processos = obter_processos()

    console.print("\nEscolha o algoritmo de escalonamento:")
    console.print("1 - FIFO (First In, First Out)")
    console.print("2 - SJF (Shortest Job First)")
    escolha = input("Digite o número correspondente à sua escolha: ")

    simular_escalonamento(escolha, processos)

    # Perguntar se o usuário quer ver o outro algoritmo também
    outro = input("\nDeseja ver o resumo com o outro algoritmo? (s/n): ").lower()
    if outro == 's':
        tipo_oposto = '2' if escolha == '1' else '1'
        simular_escalonamento(tipo_oposto, processos)

    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
