import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, PreTrainedModel, PreTrainedTokenizer
from typing import Tuple
# Define o modelo que será carregado (
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

def load_model() -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    """
    Carrega o modelo LLM local e o tokenizer do Hugging Face.
    """
    print(f"-> Carregando modelo local: {MODEL_NAME}...")
    
    try:
        # 1. Carregar o Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        
        # 2. Carregar o Modelo
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        
        print("-> Modelo carregado com sucesso.")
        return model, tokenizer
        
    except Exception as e:
        print(f"ERRO: Falha ao carregar o modelo '{MODEL_NAME}'. Verifique sua conexão e instalação.")
        print(f"Detalhes do erro: {e}")
        return None, None