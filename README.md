# 🧮 Projeto A3 – Resolução de Sistema de Equações Lineares via Escalonamento de Matrizes

## 🎯 Tema
**Tema 2:** *Resolução de sistema de equações lineares através do escalonamento de matrizes.*

---

## 📘 Introdução
Sistemas de equações lineares estão presentes em praticamente todas as áreas da ciência, engenharia, economia e tecnologia.  
Eles permitem modelar situações onde há **várias variáveis interdependentes**, como:

- Mistura de produtos (cálculo de proporções ou custos de insumos);
- Correntes elétricas em circuitos (Leis de Kirchhoff);
- Planejamento de produção;
- Equilíbrio econômico e financeiro;
- Problemas de rotas e fluxos em redes logísticas.

O **escalonamento de matrizes (eliminação de Gauss)** é um dos métodos mais utilizados para resolver esse tipo de problema de forma sistemática.  
Neste projeto, foi desenvolvido um **programa com interface gráfica em Python**, que permite **inserir os coeficientes de um sistema linear e acompanhar o passo a passo da resolução**, até encontrar as incógnitas.

---

## 🧠 Fundamentação Teórica

Um **sistema linear** com \(n\) incógnitas pode ser representado como:

\[
A \cdot X = B
\]

onde:

- \(A\) é a **matriz dos coeficientes**;
- \(X\) é o **vetor de incógnitas** (\(x_1, x_2, \dots, x_n\));
- \(B\) é o **vetor dos termos independentes**.

O **método do escalonamento (eliminação de Gauss)** transforma a matriz aumentada \([A|B]\) em uma forma **triangular superior**, aplicando operações elementares de linha:

1. Troca de linhas (para evitar pivôs nulos);
2. Multiplicação de uma linha por um escalar não nulo;
3. Subtração de múltiplos de uma linha de outra.

Depois dessa etapa, utiliza-se a **retro-substituição**, resolvendo o sistema de trás para frente:

\[
x_n = \frac{b_n'}{a_{nn}'}, \quad x_{n-1} = \frac{b_{n-1}' - a_{n-1,n}'x_n}{a_{n-1,n-1}'}, \ \text{etc.}
\]

Esse processo é determinístico e garante a solução única sempre que a matriz \(A\) for **não singular (determinante ≠ 0)**.

---

## 💻 Projeto: Programa em Python (Tkinter)

O programa foi desenvolvido em **Python**, utilizando:
- `tkinter` → para a **interface gráfica**;
- `numpy` → para operações matriciais;
- `random` → para gerar sistemas aleatórios de teste.

### 🎨 Interface do Programa

A interface é amigável e interativa:
- O usuário informa a **ordem da matriz (n)**;
- São gerados automaticamente campos para inserir os coeficientes \(A\) e o vetor \(b\);
- É possível preencher **números aleatórios de -20 a 20**;
- O sistema é resolvido **passo a passo**, com explicação textual do processo de escalonamento e retro-substituição.

---

### 🧩 Estrutura do Código

| Parte | Função |
|-------|--------|
| **1. Importações** | Importa bibliotecas (`tkinter`, `numpy`, `random`). |
| **2. Função `format_matriz_aug()`** | Formata a matriz aumentada `[A|b]` para exibição. |
| **3. Função `escalonamento_com_passos()`** | Implementa o método de **eliminação de Gauss com pivoteamento parcial**, exibindo cada passo no painel de texto. |
| **4. Classe `EscalonadorGUI`** | Controla a interface gráfica (campos, botões, eventos, resultados). |
| **5. Botões da Interface** | - **Gerar Campos**: cria a estrutura da matriz.<br> - **Gerar Aleatórios (-20 a 20)**: preenche os campos automaticamente.<br> - **Resolver Sistema**: executa o escalonamento passo a passo.<br> - **Limpar Campos**: limpa todos os campos e o texto de saída. |
| **6. Função Principal (`if __name__ == "__main__"`)** | Inicia o aplicativo. |

---

### 🧠 Exemplo de Uso

**Sistema de exemplo:**

\[
\begin{cases}
2x + y - z = 8 \\
-3x - y + 2z = -11 \\
-2x + y + 2z = -3
\end{cases}
\]

O programa executa automaticamente:
- Escalonamento (gerando matriz triangular);
- Retro-substituição;
- Exibe os valores das incógnitas \(x_1, x_2, x_3\).

---

### 📊 Resultados e Visualização

Durante a execução, o programa mostra mensagens como:

```
Matriz aumentada inicial:
   2.0000 |   1.0000 |  -1.0000  ||   8.0000
  -3.0000 |  -1.0000 |   2.0000  || -11.0000
  -2.0000 |   1.0000 |   2.0000  ||  -3.0000

↔ Troca linha 1 ↔ linha 2
→ Eliminar A[2,1] com fator = -0.6667
→ Eliminar A[3,1] com fator = -0.3333
...
x1 = 2.0000
x2 = 3.0000
x3 = -1.0000
```

Esse passo a passo ajuda o aluno a **entender o processo matemático** por trás do algoritmo.

---

## 💡 Aplicações no Cotidiano

O método de escalonamento é amplamente usado em:

| Área | Aplicação |
|------|------------|
| **Engenharia** | Cálculo de forças em estruturas e circuitos elétricos. |
| **Economia** | Equilíbrio de preços e fluxos financeiros. |
| **Computação** | Resolução de sistemas em gráficos, IA, machine learning. |
| **Ciências Naturais** | Modelagem de misturas químicas e reações. |
| **Logística** | Planejamento e distribuição de recursos. |

Assim, o projeto conecta **conceitos matemáticos abstratos com problemas reais** e o uso da **programação como ferramenta de solução prática**.

---

## 📈 Resultados

O programa foi testado com sistemas de diferentes tamanhos (2x2, 3x3, 4x4, etc.), sempre retornando corretamente as soluções numéricas e o processo de escalonamento.

Ele permite visualizar:
- Cada operação elementar de linha;
- O efeito do pivoteamento;
- A retro-substituição final.

---

## 🧾 Conclusão

O projeto demonstra que a **programação é uma poderosa aliada na compreensão dos conceitos matemáticos**.  
Através do escalonamento de matrizes, o aluno visualiza passo a passo como os sistemas lineares são resolvidos, fortalecendo a ligação entre **teoria e prática**.  

Além de resolver problemas acadêmicos, esse método é aplicável em inúmeras situações reais, tornando-se uma ferramenta essencial em **engenharia, tecnologia e ciências exatas**.

---

## ⚙️ Como Executar o Programa

1. Certifique-se de ter o **Python 3** instalado.  
2. Instale o NumPy (se necessário):
   ```bash
   pip install numpy
   ```
3. Salve o código com o nome `escalonamento_gui.py`.
4. Execute:
   ```bash
   python escalonamento_gui.py
   ```
5. Insira os dados manualmente ou use o botão **“Gerar Aleatórios (-20 a 20)”**.
6. Clique em **“Resolver Sistema”** para ver o passo a passo.

---

## 🧑‍💻 Autores
Projeto desenvolvido para a **Unidade Curricular Estruturas Matemáticas – UNIFACS (A3 – 2025.2)**  
**Tema 2:** *Resolução de sistema de equações lineares através do escalonamento de matrizes.*  

---

### 📎 Próximos Arquivos Complementares
Além deste README:
- **PowerPoint:** apresentará o contexto, teoria, código e resultados em slides.  
- **Relatório Word:** explicará detalhadamente o projeto com seções:
  1. Introdução  
  2. Fundamentação Teórica  
  3. Projeto (código e cálculos)  
  4. Resultados  
  5. Conclusão  
