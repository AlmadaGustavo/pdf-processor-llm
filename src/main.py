import sys
import pathlib
from typing import Dict, Any

# Importa os módulos principais
from cli.arguments import parse_arguments
from pdf.extractor import extract_pdf_analysis
from pdf.images import extract_pdf_images
from llm.summarize import generate_llm_summary
from utils.report import create_markdown_report

def format_analysis_output(analysis_results: Dict[str, Any]):
    """
    Formata e imprime os resultados da análise no console.
    """
    if "error" in analysis_results:
        print(f"\n[ERRO NA ANÁLISE]: {analysis_results['error']}\n")
        return
    total_pages = analysis_results["total_pages"]
    total_words = analysis_results["total_words"]
    vocabulary_size = analysis_results["vocabulary_size"]
    file_size_bytes = analysis_results["file_size_bytes"]
    top_10 = analysis_results["top_10_words"]

    print("\n============== ANÁLISE ESTRUTURAL DO PDF ==============")
    
    print(f"Número Total de Páginas: {total_pages}")
    
    print(f"Total de Palavras: {total_words:,}")
    print(f"Tamanho do Vocabulário (Distintas): {vocabulary_size:,}")
    print(f"Tamanho do Arquivo em Bytes: {file_size_bytes:,} bytes")

    print("\nLista das 10 Palavras Mais Comuns (sem Stopwords):")
    # Itera sobre a lista de tuplas (palavra, contagem)
    for rank, (word, count) in enumerate(top_10, 1):
        # Exibe o ranking, a palavra e sua contagem
        print(f"  {rank:02}. {word:<15} - {count:,} vezes") 
    print("=====================================================")
    pass

def main():
    # 1. Obter e Validar Argumentos
    args = parse_arguments()
    
    # Conversão de strings de argumento para objetos Path
    pdf_path = pathlib.Path(args.file)
    output_path = pathlib.Path(args.output)
    
    # Exemplo de verificação simples de existência
    if not pdf_path.exists():
        print(f"Erro: O arquivo PDF não foi encontrado no caminho: {pdf_path}")
        sys.exit(1)
        
    print(f"\n--- Iniciando Processamento do Arquivo: {pdf_path.name} ---\n")
    
    # 2. Executar Análise do PDF
    analysis_results = extract_pdf_analysis(pdf_path)
    
    # 3. Exibir Resultados da Análise
    format_analysis_output(analysis_results)
    
    # 4. Executar Extração de Imagens
    images_results = extract_pdf_images(pdf_path, output_path)
    
    if "error" in images_results:
         print(f"[AVISO/ERRO IMAGENS]: {images_results['error']}")
    else:
         print(f"[IMAGENS]: {images_results['images_extracted']} imagens extraídas para: {images_results['output_directory']}")

    # 5. Executar LLM Condicionalmente
    if args.summarize:
        summary = ""
        print("\n[LLM]: Gerando resumo com modelo local...")
        
        #  Obter o texto completo do dicionário de resultados
        full_text = analysis_results.get("full_text", "") 
        
        if analysis_results.get("error"):
            print("[AVISO LLM]: Análise falhou, resumo LLM não será gerado.")
        elif full_text:
            summary = generate_llm_summary(full_text)
            
            print("\n================== RESUMO (LLM) ===================")
            print(summary)
            print("===================================================\n")
        else:
            print("[AVISO LLM]: O PDF não contém texto para sumarização.")
        print("\n[RELATÓRIO]: Gerando relatório final em Markdown...")
        report_results = create_markdown_report(
            analysis_results, 
            summary, 
            output_path, 
            pdf_path
        )
        
        if report_results['status'] == 'success':
            print(f"[RELATÓRIO]: Salvo com sucesso em: {report_results['file_path']}")
        else:
            print(f"[ERRO RELATÓRIO]: {report_results['message']}")

if __name__ == '__main__':
    main()