from typing import Dict, Any, List, Tuple
import pathlib
import fitz

# Importa as funções auxiliares
from utils.text import clean_and_tokenize, count_word_frequencies, calculate_vocabulary_size, get_top_n_words
from utils.files import get_file_size_bytes 

def extract_pdf_analysis(file_path: pathlib.Path) -> Dict[str,Any]:
    results: Dict[str, Any] = {}
    full_text = ""
    detected_titles = [] 
    
    #Variável para contar a frequência de cada tamanho de fonte
    font_size_counts: Dict[float, int] = {} 
    base_font_size = 0.0
    
    # 1. Obter Tamanho do Arquivo (continua o mesmo)
    file_size_bytes = get_file_size_bytes(file_path)
    results["file_size_bytes"] = file_size_bytes

    # 2. Abrir o PDF e Processar
    try:
        doc = fitz.open(file_path)
        results["total_pages"] = doc.page_count
        
        # --- FASE 1: Encontrar o Tamanho de Fonte Mais Comum (Tamanho Base) ---
        for page_num in range(results["total_pages"]):
            page = doc.load_page(page_num)
            text_dict = page.get_text("dict") 
            
            for block in text_dict.get("blocks", []):
                if block["type"] == 0: 
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            size = round(span["size"], 1) # Arredonda o tamanho para evitar flutuantes minúsculos
                            font_size_counts[size] = font_size_counts.get(size, 0) + 1

        # Encontra o tamanho de fonte mais frequente, que é a fonte do corpo do texto.
        if font_size_counts:
            base_font_size = max(font_size_counts, key=font_size_counts.get)
            print(f"[DEBUG HEURÍSTICA]: Fonte base (mais comum) detectada: {base_font_size:.1f} pts") # Log para debug
        
        # --- FASE 2: Extração de Texto e Detecção de Títulos ---
        for page_num in range(results["total_pages"]):
            page = doc.load_page(page_num)
            full_text += page.get_text() + " "
            
            text_dict = page.get_text("dict") # Recarrega para extração detalhada
            
            for block in text_dict.get("blocks", []):
                if block["type"] == 0:
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            current_size = round(span["size"], 1)
                            
                            # Regra robusta: a fonte é um título se for claramente maior que a fonte base
                            # (Maior que a base E não é a base)
                            if current_size > base_font_size + 0.1: # +0.1 para evitar erros de arredondamento
                                text = span["text"].strip()
                                
                                # Filtros de limpeza (min length, max words)
                                if len(text) > 5 and len(text.split()) < 15: 
                                    if text not in detected_titles:
                                        detected_titles.append(text)
        
        doc.close()

    except FileNotFoundError:
        return {"error": "FileNotFound"}
    except Exception as e:
        return {"error": str(e)}
    

    # 3. Processamento de Texto e Análise (usa o full_text extraído no loop)
    # Garante que full_text não esteja vazio
    if not full_text.strip():
        return {"error": "O PDF está vazio ou não contém texto legível."}

    tokens: List[str] = clean_and_tokenize(full_text)

    results["total_words"] = len(tokens)
    word_frequencies: Dict[str, int] = count_word_frequencies(tokens)
    results["vocabulary_size"] = calculate_vocabulary_size(tokens)
    results["top_10_words"] = get_top_n_words(word_frequencies, n=10)
    
    # Adiciona os resultados finais (Obrigatório e Opcional)
    results["full_text"] = full_text
    results["detected_titles"] = detected_titles # títulos

    # 4. Retornar os Resultados
    return results