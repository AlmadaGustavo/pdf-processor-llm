# Desafio Python - Processamento de PDF com LLM Local

## 1. Visão Geral do Projeto

Este projeto implementa uma Ferramenta de Linha de Comando (CLI) em Python para processar arquivos PDF em português. O objetivo principal é demonstrar proficiência em engenharia de software, modularização, manipulação de arquivos binários (PDFs) e integração com modelos de Linguagem de Grande Escala (LLM) rodando **localmente** (usando a biblioteca Hugging Face).

O projeto atinge a excelência ao cobrir todos os requisitos obrigatórios e a maioria dos opcionais de alta valorização, como a **detecção robusta de estrutura** e a **geração organizada de um relatório final unificado em Markdown**.

## 2. Estrutura do Projeto e Arquitetura

O projeto segue estritamente o princípio de Separação de Responsabilidades (S.O.L.I.D.), com uma arquitetura coesa e modular, garantindo fácil manutenção e testes.

```
pdf-processor-llm/ ├── src/ │   ├── cli/ │   │   └── arguments.py # Leitura e parsing de argumentos CLI (argparse) │   ├── llm/ │   │   ├── model.py # Carregamento do modelo LLM local (sshleifer/distilbart-cnn-12-6) │   │   └── summarize.py # Lógica de geração do resumo e tratamento de PDF grandes (truncation) │   ├── pdf/ │   │   ├── extractor.py # Análise de Métricas, Extração de Texto e Detecção de Títulos (Heurística Robusta) │   │   └── images.py # Extração de Imagens (Com tratamento de exceção robusto para XREFs falsos) │   ├── utils/ │   │   ├── files.py # Funções auxiliares de I/O (tamanho em bytes, etc.) │   │   ├── report.py # Geração e organização do relatório unificado em Markdown │   │   └── text.py # Funções auxiliares de processamento de texto (tokenização, stopwords, frequência) │   └── main.py # Orquestrador principal (ponto de entrada) e fluxo de trabalho └── requirements.txt # Dependências do projeto (PyMuPDF, torch, transformers)
```
---

## 3. Instalação e Uso

### 3.1. Instalação

O projeto requer Python 3.8+ e as dependências listadas em `requirements.txt`.

1.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 3.2. Argumentos CLI

| Opção | Nome Longo | Tipo | Obrigatório | Padrão | Descrição |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `-f` | `--file` | `str` | Sim | N/A | Caminho para o arquivo PDF de entrada. |
| `-o` | `--output` | `str` | Não | `output/` | Diretório de saída base para artefatos. |
| | `--summarize` | `flag` | Não | `False` | Ativa a geração do resumo LLM e o Relatório Final. |

### 3.3. Exemplo de Execução Completa

A execução completa processa o PDF e salva todas as saídas (imagens e relatório) em um **subdiretório organizado**, nomeado após o arquivo PDF.

```bash
python src/main.py -f "caminho/para/seu/arquivo.pdf" --summarize

--- Iniciando Processamento do Arquivo: MSL_1 - Documentos Google.pdf ---

[DEBUG HEURÍSTICA]: Fonte base (mais comum) detectada: 12.0 pts

============== ANÁLISE ESTRUTURAL DO PDF ==============
Número Total de Páginas: 18
Total de Palavras: 5,448
Tamanho do Vocabulário (Distintas): 1,344
Tamanho do Arquivo em Bytes: 294,796 bytes

Lista das 10 Palavras Mais Comuns (sem Stopwords):
  01. modelos           - 65 vezes
  02. esforço           - 62 vezes
...
=====================================================
[IMAGENS]: 3 imagens extraídas para: output\MSL_1 - Documentos Google

[LLM]: Gerando resumo com modelo local...
-> Carregando modelo local: sshleifer/distilbart-cnn-12-6...
-> Modelo carregado com sucesso.

================== RESUMO (LLM) ===================
Aplicações de Aplicativos Móveis: Um’so Mapeamento Sistemático da Literatura . ...
===================================================

[RELATÓRIO]: Gerando relatório final em Markdown...
[RELATÓRIO]: Salvo com sucesso em: output\MSL_1 - Documentos Google\relatorio_analise.md
```
## 4. O que gostaria que fosse avaliado
    
Gostaria que a avaliação se concentrasse nos seguintes pilares de qualidade, que demonstram o domínio das melhores práticas de Engenharia de Software e o atendimento completo aos requisitos obrigatórios e opcionais avançados:

1. Arquitetura e Engenharia de Software (Modularização)
Modularização e Arquitetura (SOLID): O código está estritamente organizado em módulos de responsabilidade única (src/cli, src/llm, src/pdf, src/utils), o que garante a coesão, facilita a manutenção e permite a escalabilidade.

Visibilidade e Logs: O código utiliza logs (mensagens informativas/debug no console) de forma estratégica, oferecendo total visibilidade do fluxo de execução, desde o carregamento do modelo até o debug da heurística de extração de títulos.

Controle de Versão: Inclusão de um arquivo .gitignore seguindo as melhores práticas, ignorando virtual environments e os grandes diretórios de saída (output/).

2. Recursos Avançados e Robustez
LLM Local: Implementação do resumo utilizando um modelo LLM rodando localmente (sshleifer/distilbart-cnn-12-6), um requisito cumprido com o tratamento de truncation para documentos longos.

Tratamento de Imagens Robusto: A função de extração de imagens inclui tratamento de exceção (try/except) para ignorar XREFs falsos (not an image), evitando crashes e garantindo que apenas arquivos de imagem válidos sejam salvos.

Detecção de Estrutura: Implementação de uma heurística de títulos aprimorada que calcula a fonte base do corpo do texto e usa essa métrica para identificar títulos de forma precisa.

3. Organização do Output
Salvamento Organizado do Relatório: O projeto gera um relatório final unificado em Markdown (relatorio_analise.md) e salva este documento, juntamente com as imagens extraídas, em um subdiretório dedicado dentro de output/, nomeado a partir do PDF de entrada, garantindo a organização do projeto."