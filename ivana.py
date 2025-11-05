import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import random

# ---------- Funções numéricas com saída passo-a-passo ----------
def format_matriz_aug(Aug):
    """Formata a matriz aumentada para exibição."""
    lines = []
    n, m = Aug.shape
    for i in range(n):
        row = " | ".join(f"{Aug[i, j]:8.4f}" for j in range(m-1))
        row += "  ||  " + f"{Aug[i, -1]:8.4f}"
        lines.append(row)
    return "\n".join(lines)

def escalonamento_com_passos(A, b, text_widget):
    """Executa o escalonamento e mostra os passos detalhados."""
    n = len(b)
    Aug = np.hstack([A.astype(float), b.reshape(-1, 1)])
    text_widget.insert(tk.END, "Matriz aumentada inicial:\n")
    text_widget.insert(tk.END, format_matriz_aug(Aug) + "\n\n")
    text_widget.see(tk.END)

    for i in range(n):
        # Pivoteamento parcial
        pivot_row = i + np.argmax(np.abs(Aug[i:, i]))
        if abs(Aug[pivot_row, i]) < 1e-12:
            raise ValueError(f"Pivô (coluna {i+1}) é zero — sistema singular.")
        if pivot_row != i:
            text_widget.insert(tk.END, f"↔ Troca linha {i+1} ↔ linha {pivot_row+1}\n")
            Aug[[i, pivot_row], :] = Aug[[pivot_row, i], :]
            text_widget.insert(tk.END, format_matriz_aug(Aug) + "\n\n")

        piv = Aug[i, i]
        for j in range(i+1, n):
            fator = Aug[j, i] / piv
            if abs(fator) < 1e-15:
                continue
            text_widget.insert(tk.END, f"→ Eliminar A[{j+1},{i+1}] com fator = {fator:.4f}\n")
            Aug[j, :] = Aug[j, :] - fator * Aug[i, :]
            Aug[j, np.abs(Aug[j, :]) < 1e-14] = 0.0
            text_widget.insert(tk.END, format_matriz_aug(Aug) + "\n\n")
            text_widget.see(tk.END)

    text_widget.insert(tk.END, "Matriz triangular superior:\n")
    text_widget.insert(tk.END, format_matriz_aug(Aug) + "\n\n")

    # Retro-substituição
    x = np.zeros(n)
    text_widget.insert(tk.END, "Retro-substituição:\n")
    for i in range(n-1, -1, -1):
        soma = np.dot(Aug[i, i+1:n], x[i+1:n])
        x[i] = (Aug[i, -1] - soma) / Aug[i, i]
        text_widget.insert(
            tk.END,
            f"x{i+1} = ({Aug[i,-1]:.4f} - {soma:.4f}) / {Aug[i,i]:.4f} = {x[i]:.4f}\n"
        )
    text_widget.insert(tk.END, "\nSolução final:\n")
    for i in range(n):
        text_widget.insert(tk.END, f"x{i+1} = {x[i]:.4f}\n")
    text_widget.insert(tk.END, "\n" + "-"*60 + "\n\n")
    text_widget.see(tk.END)
    return x

# ---------- Interface gráfica ----------
class EscalonadorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Resolução de Sistema Linear - Escalonamento (passo a passo)")
        master.geometry("820x620")

        tk.Label(master, text="Resolução de Sistema de Equações Lineares",
                 font=("Arial", 14, "bold")).pack(pady=6)
        tk.Label(master, text="Método: Escalonamento (Eliminação de Gauss) com pivoteamento parcial",
                 font=("Arial", 10)).pack()

        topo = tk.Frame(master)
        topo.pack(pady=8)

        tk.Label(topo, text="Ordem da matriz (n):").grid(row=0, column=0, padx=5)
        self.entrada_ordem = tk.Entry(topo, width=4)
        self.entrada_ordem.insert(0, "3")
        self.entrada_ordem.grid(row=0, column=1, padx=4)

        tk.Button(topo, text="Gerar Campos", command=self.criar_campos).grid(row=0, column=2, padx=6)
        tk.Button(topo, text="Limpar Saída", command=self.limpar_saida).grid(row=0, column=3, padx=6)

        self.frame_matriz = tk.Frame(master)
        self.frame_matriz.pack(pady=10)

        tk.Label(master, text="Passo a passo:").pack()
        self.text_saida = scrolledtext.ScrolledText(master, width=95, height=18, font=("Courier", 10))
        self.text_saida.pack(padx=10, pady=6)

        self.criar_campos_inicial()

    def criar_campos_inicial(self):
        try:
            n = int(self.entrada_ordem.get())
        except:
            n = 3
            self.entrada_ordem.delete(0, tk.END)
            self.entrada_ordem.insert(0, "3")
        self._criar_campos(n)

    def criar_campos(self):
        try:
            n = int(self.entrada_ordem.get())
            if n <= 0 or n > 10:
                messagebox.showwarning("Aviso", "Escolha n entre 1 e 10.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido para n.")
            return
        self._criar_campos(n)

    def _criar_campos(self, n):
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()
        self.entradas_A, self.entradas_b = [], []

        tk.Label(self.frame_matriz, text="Coeficientes da matriz A:").grid(row=0, column=0, columnspan=n)
        for i in range(n):
            linha = []
            for j in range(n):
                e = tk.Entry(self.frame_matriz, width=8, justify="center")
                e.grid(row=i+1, column=j, padx=3, pady=2)
                linha.append(e)
            self.entradas_A.append(linha)

        tk.Label(self.frame_matriz, text="Termos independentes (b):").grid(row=0, column=n+1, padx=10)
        for i in range(n):
            e = tk.Entry(self.frame_matriz, width=8, justify="center")
            e.grid(row=i+1, column=n+1, padx=10)
            self.entradas_b.append(e)

        btn_frame = tk.Frame(self.frame_matriz)
        btn_frame.grid(row=n+2, column=0, columnspan=n+2, pady=8)
        tk.Button(btn_frame, text="Resolver Sistema", command=self.resolver).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Gerar Aleatórios (-20 a 20)", command=self.preencher_aleatorio).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Limpar Campos", command=self.limpar_campos).grid(row=0, column=2, padx=6)

    def preencher_aleatorio(self):
        """Preenche A e b com números aleatórios entre -20 e 20."""
        n = len(self.entradas_A)
        for i in range(n):
            for j in range(n):
                val = random.randint(-20, 20)
                self.entradas_A[i][j].delete(0, tk.END)
                self.entradas_A[i][j].insert(0, str(val))
            val_b = random.randint(-20, 20)
            self.entradas_b[i].delete(0, tk.END)
            self.entradas_b[i].insert(0, str(val_b))
        # limpa o passo a passo antigo ao gerar novo sistema
        self.text_saida.delete(1.0, tk.END)

    def limpar_campos(self):
        """Limpa todos os campos e o texto do passo a passo."""
        for row in self.entradas_A:
            for e in row:
                e.delete(0, tk.END)
        for e in self.entradas_b:
            e.delete(0, tk.END)
        self.text_saida.delete(1.0, tk.END)

    def limpar_saida(self):
        """Limpa apenas o texto do passo a passo."""
        self.text_saida.delete(1.0, tk.END)

    def resolver(self):
        try:
            n = len(self.entradas_A)
            if n == 0:
                messagebox.showerror("Erro", "Gere os campos primeiro.")
                return

            A = np.zeros((n, n))
            b = np.zeros(n)
            for i in range(n):
                for j in range(n):
                    s = self.entradas_A[i][j].get().strip()
                    A[i, j] = float(s) if s else 0.0
                sb = self.entradas_b[i].get().strip()
                b[i] = float(sb) if sb else 0.0

            self.text_saida.insert(tk.END, f"==== Novo sistema {n}x{n} ====\n")
            escalonamento_com_passos(A, b, self.text_saida)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# ---------- Inicialização ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = EscalonadorGUI(root)
    root.mainloop()
