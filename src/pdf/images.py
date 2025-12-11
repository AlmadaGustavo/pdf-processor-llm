import pathlib
import fitz
import os
from typing import Dict, Any, List, Optional

def extract_pdf_images(file_path: pathlib.Path, output_dir_base: pathlib.Path) -> Dict[str, Any]:
    """
    Identifica e extrai todas as imagens contidas no PDF.
    Cria um subdiretório baseado no nome do arquivo PDF para armazenar as imagens.
    """
    image_count = 0
    # 1. Definir o Diretório de Saída (imagens/<nome-arquivo-pdf>/)
    pdf_name_stem = file_path.stem # Nome do arquivo sem extensão
    output_dir = output_dir_base / pdf_name_stem
    
    # 2. Iterar sobre os objetos internos do PDF (XREF) para encontrar imagens
    try:
        with fitz.open(file_path) as doc:
            lenXREF = doc.xref_length()
            processed_images = set()

            # 2. Iterar sobre os objetos internos do PDF (XREF) para encontrar imagens
            for xref in range(1, lenXREF):
                
                imgdict = None # Inicializa o dicionário de imagem
                
                # Bloco TRY/EXCEPT para isolar a extração de imagem problemática
                try:
                    imgdict = doc.extract_image(xref) 
                except Exception as e:
                    # Captura erros como "not an image" ou "corrupted stream"
                    continue # Pula para o próximo XREF

                if imgdict and 'image' in imgdict: # Se for um objeto de imagem válido
                    
                    image_id = (imgdict.get('width'), imgdict.get('height'), imgdict.get('colorspace'))
                    
                    if image_id in processed_images:
                        continue
                    
                    processed_images.add(image_id)
                    
                    img_data = imgdict["image"]
                    # Use .get('ext', 'png') para lidar com 'ext' faltante/vazio de forma mais limpa
                    img_ext = imgdict.get('ext', 'png')
                    
                    # 3. Salvar a imagem com um nome único
                    image_filename = f"{pdf_name_stem}_img_{xref}.{img_ext}"
                    output_path = output_dir / image_filename
                    
                    with open(output_path, "wb") as img_file:
                        img_file.write(img_data)
                        
                    image_count += 1
            
    except FileNotFoundError:
        return {"error": "FileNotFound"}
    except Exception as e:
        # Este é o catch para erros mais amplos (abrir o arquivo, etc.)
        return {"error": f"Erro fatal durante o processamento do PDF: {e}"}
        
    return {"status": "success", "images_extracted": image_count, "output_directory": str(output_dir)}