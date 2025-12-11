import pathlib
from typing import Dict, Any

def create_markdown_report(
    analysis_results: Dict[str, Any], 
    summary_text: str, 
    base_output_path: pathlib.Path, 
    pdf_path: pathlib.Path        
) -> Dict[str, Any]:
    """
    Gera um relatório final em formato Markdown com todas as análises e resumo,
    salvando em um subdiretório nomeado após o arquivo PDF.
    """
    
    # 1. Montar o Conteúdo do Relatório 
    report_content = f"# Relatório de Análise do PDF\n\n"
    report_content += f"**Arquivo Processado:** `{pdf_path.name}`\n\n" 
    
    # --- Seção 1: Análise Estrutural ---
    report_content += "## 1. Análise Estrutural\n\n"
    report_content += "| Métrica | Valor |\n"
    report_content += "| :--- | :--- |\n"
    report_content += f"| Páginas | {analysis_results['total_pages']} |\n"
    report_content += f"| Palavras (Total) | {analysis_results['total_words']:,} |\n"
    report_content += f"| Vocabulário (Distinto) | {analysis_results['vocabulary_size']:,} |\n"
    report_content += f"| Tamanho (Bytes) | {analysis_results['file_size_bytes']:,} |\n\n"
    
    # --- Seção 2: Detecção de Títulos ---
    titles = analysis_results.get("detected_titles", [])
    if titles:
        report_content += "## 2. Detecção de Títulos e Seções\n\n"
        report_content += "### Títulos Detectados\n"
        for title in titles:
            report_content += f"- **{title}**\n"
        report_content += "\n"

    # --- Seção 3: Palavras-Chave ---
    report_content += "## 3. Top 10 Palavras-Chave\n\n"
    for rank, (word, count) in enumerate(analysis_results['top_10_words'], 1):
        report_content += f"{rank}. **{word}** ({count:,} vezes)\n"
    report_content += "\n"

    # --- Seção 4: Resumo LLM ---
    report_content += "## 4. Resumo (LLM Local)\n\n"
    formatted_summary = summary_text.replace('\n', '\n> ')
    report_content += f"> {formatted_summary}\n\n"
    
    # 2. Salvar o Arquivo
    
    # Define o subdiretório baseado no nome do PDF 
    pdf_name_without_extension = pdf_path.stem 
    report_directory = base_output_path / pdf_name_without_extension
    
    # Garante que o subdiretório de saída existe (igual ao que a extração de imagens faz)
    report_directory.mkdir(parents=True, exist_ok=True)
    
    # Define o nome do arquivo de saída dentro do novo diretório
    report_file = report_directory / "relatorio_analise.md"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        # Retorna o caminho completo e correto
        return {"status": "success", "file_path": str(report_file)}
    except Exception as e:
        return {"status": "error", "message": f"Falha ao salvar relatório: {e}"}