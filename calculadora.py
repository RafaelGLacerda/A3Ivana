import re
import cmath
import tkinter as tk
from tkinter import messagebox, scrolledtext

# ------------------ Classe Nó da Árvore ------------------
class No:
    def __init__(self, valor, esquerdo=None, direito=None):
        self.valor = valor
        self.esquerdo = esquerdo
        self.direito = direito

    def __repr__(self):
        if self.esquerdo and self.direito:
            return f"({self.esquerdo} {self.valor} {self.direito})"
        elif self.esquerdo:
            return f"({self.valor}{self.esquerdo})"
        return str(self.valor)


# ------------------ Parser e construção da árvore ------------------
class ExpressaoComplexa:
    def __init__(self, expr):
        self.expr = expr.replace(" ", "")
        self.tokens = self.tokenizar(self.expr)
        self.pos = 0
        self.arvore = self.parse_expressao()

    def tokenizar(self, expr):
        padrao = r'(\*\*|[+\-*/()√]|conj|[A-Za-z_]\w*|\d+\.?\d*|i)'
        return re.findall(padrao, expr)

    def olhar(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self):
        token = self.olhar()
        self.pos += 1
        return token

    def parse_expressao(self):
        no = self.parse_termo()
        while self.olhar() in ('+', '-'):
            op = self.consumir()
            direito = self.parse_termo()
            no = No(op, no, direito)
        return no

    def parse_termo(self):
        no = self.parse_fator()
        while self.olhar() in ('*', '/', '**'):
            op = self.consumir()
            direito = self.parse_fator()
            no = No(op, no, direito)
        return no

    def parse_fator(self):
        token = self.olhar()

        if token == '(':
            self.consumir()
            no = self.parse_expressao()
            if self.consumir() != ')':
                raise ValueError("Erro de parênteses")
            return no

        elif token == '√':
            self.consumir()
            interno = self.parse_fator()
            return No('√', interno)

        elif token == 'conj':
            self.consumir()
            if self.consumir() != '(':
                raise ValueError("Falta '(' após conj")
            interno = self.parse_expressao()
            if self.consumir() != ')':
                raise ValueError("Falta ')' após conj(...)")
            return No('conj', interno)

        elif re.match(r'[A-Za-z]', token):  # variável
            self.consumir()
            return No(token)

        else:  # número
            self.consumir()
            if token == 'i':
                return No(complex(0, 1))
            if self.olhar() == 'i':
                self.consumir()
                return No(complex(0, float(token)))
            try:
                return No(complex(float(token), 0))
            except:
                raise ValueError(f"Valor inválido: {token}")


# ------------------ Calculadora de expressões complexas ------------------
class CalculadoraComplexa:
    def __init__(self, expr):
        self.expr = ExpressaoComplexa(expr)
        self.vars = {}

    def avaliar(self, no):
        if isinstance(no.valor, complex):
            return no.valor

        if isinstance(no.valor, str) and re.match(r'^[A-Za-z_]\w*$', no.valor):
            if no.valor not in self.vars:
                val = simple_input(f"Digite o valor da variável {no.valor} (ex: 3+2i): ")
                self.vars[no.valor] = self.parse_complexo(val)
            return self.vars[no.valor]

        if no.valor == '√':
            return cmath.sqrt(self.avaliar(no.esquerdo))
        if no.valor == 'conj':
            v = self.avaliar(no.esquerdo)
            return complex(v.real, -v.imag)

        esquerdo = self.avaliar(no.esquerdo)
        direito = self.avaliar(no.direito)

        if no.valor == '+':
            return esquerdo + direito
        elif no.valor == '-':
            return esquerdo - direito
        elif no.valor == '*':
            return esquerdo * direito
        elif no.valor == '/':
            if direito == 0:
                raise ZeroDivisionError("Divisão por zero")
            return esquerdo / direito
        elif no.valor == '**':
            return esquerdo ** direito
        else:
            raise ValueError(f"Operador inválido: {no.valor}")

    def parse_complexo(self, texto):
        texto = texto.replace('i', 'j')
        return complex(texto)

    def executar(self):
        return self.avaliar(self.expr.arvore)


# ------------------ Interface Tkinter ------------------
def simple_input(msg):
    top = tk.Toplevel()
    top.title("Variável necessária")
    tk.Label(top, text=msg, font=("Segoe UI", 11)).pack(padx=10, pady=10)
    entrada = tk.Entry(top, font=("Segoe UI", 11))
    entrada.pack(padx=10, pady=5)
    resultado = []

    def confirmar():
        resultado.append(entrada.get())
        top.destroy()

    tk.Button(top, text="OK", command=confirmar, bg="#0078D7", fg="white", font=("Segoe UI", 10)).pack(pady=5)
    top.grab_set()
    top.wait_window()
    return resultado[0] if resultado else ""


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Números Complexos v3.0")
        self.root.geometry("520x650")
        self.root.resizable(False, False)

        frame = tk.Frame(root, bd=2, relief="groove", padx=10, pady=10)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Primeira expressão
        tk.Label(frame, text="Expressão 1:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.entrada1 = tk.Entry(frame, font=("Consolas", 12))
        self.entrada1.pack(fill="x", pady=5)

        # Segunda expressão (para comparação)
        tk.Label(frame, text="Expressão 2 (para comparar):", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 0))
        self.entrada2 = tk.Entry(frame, font=("Consolas", 12))
        self.entrada2.pack(fill="x", pady=5)

        # Botões principais
        botoes = tk.Frame(frame)
        botoes.pack(pady=5)
        self.botao_calc = tk.Button(botoes, text="Calcular 1", bg="#4A90E2", fg="white",
                                    font=("Segoe UI", 11, "bold"), width=12, command=self.calcular)
        self.botao_calc.grid(row=0, column=0, padx=5)
        self.botao_cmp = tk.Button(botoes, text="Comparar", bg="#009688", fg="white",
                                   font=("Segoe UI", 11, "bold"), width=12, command=self.comparar)
        self.botao_cmp.grid(row=0, column=1, padx=5)
        self.botao_clear = tk.Button(botoes, text="Limpar", bg="#E94E4E", fg="white",
                                     font=("Segoe UI", 11, "bold"), width=12, command=self.limpar)
        self.botao_clear.grid(row=0, column=2, padx=5)

        # Árvore e resultado
        tk.Label(frame, text="Árvore da expressão 1:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.texto_arvore1 = scrolledtext.ScrolledText(frame, height=4, font=("Consolas", 10))
        self.texto_arvore1.pack(fill="x", pady=5)

        tk.Label(frame, text="Árvore da expressão 2:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.texto_arvore2 = scrolledtext.ScrolledText(frame, height=4, font=("Consolas", 10))
        self.texto_arvore2.pack(fill="x", pady=5)

        tk.Label(frame, text="Resultado:", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.resultado = tk.Label(frame, text="", font=("Consolas", 12), fg="#333")
        self.resultado.pack(anchor="w", pady=5)

    # ----- Função principal: calcular apenas a primeira expressão -----
    def calcular(self):
        expr = self.entrada1.get()
        try:
            calc = CalculadoraComplexa(expr)
            res = calc.executar()
            self.texto_arvore1.delete(1.0, tk.END)
            self.texto_arvore1.insert(tk.END, str(calc.expr.arvore))
            self.resultado.config(text=f"Resultado: {res}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ----- Função de comparação de duas expressões -----
    def comparar(self):
        expr1 = self.entrada1.get().strip()
        expr2 = self.entrada2.get().strip()
        if not expr1 or not expr2:
            messagebox.showwarning("Aviso", "Digite as duas expressões para comparar.")
            return
        try:
            calc1 = CalculadoraComplexa(expr1)
            calc2 = CalculadoraComplexa(expr2)
            res1 = calc1.executar()
            res2 = calc2.executar()
            self.texto_arvore1.delete(1.0, tk.END)
            self.texto_arvore2.delete(1.0, tk.END)
            self.texto_arvore1.insert(tk.END, str(calc1.expr.arvore))
            self.texto_arvore2.insert(tk.END, str(calc2.expr.arvore))
            if abs(res1 - res2) < 1e-9:
                self.resultado.config(text=f"As expressões são EQUIVALENTES.\nValor: {res1}", fg="#008000")
            else:
                self.resultado.config(text=f"As expressões são DIFERENTES.\nExpr1: {res1}\nExpr2: {res2}", fg="#E91E63")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ----- Limpar tudo -----
    def limpar(self):
        self.entrada1.delete(0, tk.END)
        self.entrada2.delete(0, tk.END)
        self.texto_arvore1.delete(1.0, tk.END)
        self.texto_arvore2.delete(1.0, tk.END)
        self.resultado.config(text="", fg="#333")


# ------------------ Execução principal ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
