import json
import os

caminho = "data/biblia.json"
with open(caminho, "r", encoding="utf-8-sig") as f:
    dados = json.load(f)

print("Tipo:", type(dados))
print("Primeiros 3 itens:")
if isinstance(dados, list):
    for i, livro in enumerate(dados[:3]):
        print(f"\nLivro {i+1}: {list(livro.keys())}")
        if "capitulos" in livro:
            print("  Primeiro capítulo:", livro["capitulos"][0].keys())
elif isinstance(dados, dict):
    print("Chaves principais:", list(dados.keys()))
    # Verifica se tem 'books' ou algo parecido