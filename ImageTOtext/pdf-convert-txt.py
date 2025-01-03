import pytesseract
from PIL import Image
import os

# Configurar o caminho do executável Tesseract (no Windows, se necessário)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Pasta onde estão as imagens
pasta_imagens = "imagensparatexto"

# Inicializar variável para armazenar todo o texto extraído
texto_completo = ""

# Processar todas as imagens na pasta
for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):  # Verificar formatos suportados
        caminho_imagem = os.path.join(pasta_imagens, nome_arquivo)
        
        # Abrir e processar a imagem
        imagem = Image.open(caminho_imagem)
        texto = pytesseract.image_to_string(imagem, lang="por")
        
        # Adicionar o texto ao resultado final
        texto_completo += f"\n--- Texto extraído da imagem: {nome_arquivo} ---\n"
        texto_completo += texto + "\n"

# Salvar todo o texto em um arquivo .txt
with open("resultado_completo.txt", "w", encoding="utf-8") as arquivo_txt:
    arquivo_txt.write(texto_completo)

print("Texto extraído com sucesso de todas as imagens e salvo em 'resultado_completo.txt'")
