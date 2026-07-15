import os
import json
from gtts import gTTS

# ---------- Configurações ----------
CAMINHO_JSON = "data/oracoes.json"
PASTA_AUDIO = "app/assets/audio"
IDIOMA = "pt"  # português

# ---------- Criar pasta de áudio se não existir ----------
os.makedirs(PASTA_AUDIO, exist_ok=True)

# ---------- Carregar orações ----------
try:
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        oracoes = json.load(f)
    print(f"✅ Carregado {CAMINHO_JSON} com sucesso.")
except FileNotFoundError:
    print(f"❌ Arquivo {CAMINHO_JSON} não encontrado. Verifique o caminho.")
    exit(1)
except Exception as e:
    print(f"❌ Erro ao ler {CAMINHO_JSON}: {e}")
    exit(1)

# ---------- Gerar áudios ----------
total = 0
gerados = 0
erros = 0

for categoria, lista in oracoes.items():
    for oracao in lista:
        titulo = oracao.get("titulo", "")
        texto = oracao.get("texto", "")
        if not titulo or not texto:
            print(f"⚠️ Oração sem título ou texto ignorada (categoria: {categoria})")
            continue
        
        # Nome do arquivo: remove caracteres inválidos para Windows
        nome_arquivo = titulo.replace("/", "-").replace("\\", "-").replace(":", "-").replace("*", "-").replace("?", "-").replace("\"", "-").replace("<", "-").replace(">", "-").replace("|", "-")
        caminho_audio = os.path.join(PASTA_AUDIO, f"{nome_arquivo}.mp3")
        
        # Se o arquivo já existe, pula (opcional – remova o if para regerar tudo)
        if os.path.exists(caminho_audio):
            print(f"⏩ Áudio já existe: {nome_arquivo}.mp3 (pulando)")
            continue
        
        total += 1
        try:
            print(f"🎤 Gerando: {titulo} ...")
            tts = gTTS(text=texto, lang=IDIOMA, slow=False)
            tts.save(caminho_audio)
            print(f"   ✅ Salvo em: {caminho_audio}")
            gerados += 1
        except Exception as e:
            print(f"   ❌ Erro ao gerar {titulo}: {e}")
            erros += 1

# ---------- Resumo ----------
print("\n" + "="*50)
print(f"📊 Resumo:")
print(f"   Total de áudios gerados: {gerados}")
print(f"   Pulados (já existiam): {total - gerados - erros}")
print(f"   Erros: {erros}")
print("="*50)
print("✅ Processo concluído!")