from typing import Tuple, Any, Dict
from .model import load_model 

def generate_llm_summary(full_text: str) -> str:
    """
    Gera um resumo do texto completo usando o LLM local.
    """
    # 1. Carregar o Modelo e Tokenizer (ou passá-los como argumentos se for mais eficiente)
    model, tokenizer = load_model()
    
    if model is None:
        return "Erro: Modelo LLM não pôde ser carregado."
    
    # 2. Preparar a Entrada (Tokenizar)
    inputs = tokenizer.encode(full_text, return_tensors='pt', truncation=True) 

    # 3. Gerar o Resumo
    summary_ids = model.generate(
        inputs, 
        max_length=500, 
        min_length=50, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True
    )

    # 4. Decodificar e Retornar
    # Usa o tokenizer.decode para converter os IDs de volta para texto.
    summary = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    
    return summary