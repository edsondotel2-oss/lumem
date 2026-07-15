import flet as ft
import json
import os
from datetime import datetime, timedelta
import random

# ---------- Carregar dados ----------
def carregar_biblia():
    caminho = "biblia.json"
    try:
        with open(caminho, "r", encoding="utf-8-sig") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return [
            {
                "nome": "Gênesis",
                "abreviacao": "Gn",
                "capitulos": [
                    {
                        "numero": 1,
                        "versiculos": [
                            {"numero": 1, "texto": "No princípio, Deus criou os céus e a terra."},
                            {"numero": 2, "texto": "A terra era sem forma e vazia..."},
                            {"numero": 3, "texto": "Disse Deus: Haja luz. E houve luz."}
                        ]
                    }
                ]
            },
            {
                "nome": "Mateus",
                "abreviacao": "Mt",
                "capitulos": [
                    {
                        "numero": 1,
                        "versiculos": [
                            {"numero": 1, "texto": "Livro da geração de Jesus Cristo..."},
                            {"numero": 2, "texto": "Abraão gerou Isaque..."}
                        ]
                    }
                ]
            }
        ]
    except Exception as e:
        print(f"Erro ao carregar Bíblia: {e}")
        return []

    biblia_convertida = []
    for livro in dados:
        novo_livro = {
            "nome": livro.get("name", ""),
            "abreviacao": livro.get("abbrev", ""),
            "capitulos": []
        }
        for i, capitulo in enumerate(livro.get("chapters", []), start=1):
            versiculos = []
            for j, texto in enumerate(capitulo, start=1):
                versiculos.append({
                    "numero": j,
                    "texto": texto
                })
            novo_livro["capitulos"].append({
                "numero": i,
                "versiculos": versiculos
            })
        biblia_convertida.append(novo_livro)
    return biblia_convertida

def carregar_oracoes():
    caminho = os.path.join("data", "oracoes.json")
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "Manhã": [
                {"titulo": "Oração da Manhã", "texto": "Senhor, agradeço por mais este dia que começa. Que a Tua luz guie meus passos e que eu possa ser instrumento do Teu amor. Amém."},
                {"titulo": "Oferecimento do Dia", "texto": "Ofereço este dia a Deus, com todas as minhas ações, pensamentos e palavras. Que tudo seja para Sua glória. Amém."}
            ],
            "Noite": [
                {"titulo": "Oração da Noite", "texto": "Senhor, agradeço pelo dia que passou. Perdoa minhas falhas e concede um sono tranquilo. Amém."},
                {"titulo": "Exame de Consciência", "texto": "Senhor, examino meu coração: onde pequei, perdoa-me; onde acertei, agradeço. Concede-me a graça de recomeçar amanhã. Amém."}
            ],
            "Família": [
                {"titulo": "Oração pela Família", "texto": "Deus, abençoa minha família. Que haja união, amor e respeito entre todos. Amém."}
            ],
            "Saúde": [
                {"titulo": "Oração pela Saúde", "texto": "Senhor, cura os enfermos e fortalece os que sofrem. Dá saúde ao meu corpo e à minha alma. Amém."}
            ],
            "Momentos Difíceis": [
                {"titulo": "Oração na Aflição", "texto": "Senhor, estou passando por um momento difícil. Dá-me força e esperança para superar esta provação. Amém."},
                {"titulo": "Oração de Confiança", "texto": "Confio em Ti, Senhor, mesmo quando não entendo os caminhos. Tua graça me basta. Amém."}
            ]
        }

# ---------- App principal ----------
def main(page: ft.Page):
    page.title = "Lumem"
    page.assets_dir = "assets"   # 🔥 LINHA NOVA
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 700
    page.window_min_width = 600
    page.window_min_height = 500
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_50

    biblia_dados = carregar_biblia()
    oracoes_dados = carregar_oracoes()

    # ---------- Favoritos ----------
    favoritos_lista = []

    def carregar_favoritos():
        try:
            favs = page.client_storage.get("favoritos")
            if favs is not None:
                if isinstance(favs, str):
                    favoritos_lista[:] = json.loads(favs)
                else:
                    favoritos_lista[:] = favs
                return
        except:
            pass
        try:
            favs = page.session.get("favoritos")
            if favs is not None:
                if isinstance(favs, str):
                    favoritos_lista[:] = json.loads(favs)
                else:
                    favoritos_lista[:] = favs
        except:
            pass

    def salvar_favoritos():
        dados = json.dumps(favoritos_lista)
        try:
            page.client_storage.set("favoritos", dados)
        except:
            pass
        try:
            page.session.set("favoritos", dados)
        except:
            pass

    def obter_favoritos():
        return favoritos_lista

    def adicionar_favorito(ref):
        if ref not in favoritos_lista:
            favoritos_lista.append(ref)
            salvar_favoritos()

    def remover_favorito(ref):
        if ref in favoritos_lista:
            favoritos_lista.remove(ref)
            salvar_favoritos()

    def eh_favorito(ref):
        return ref in favoritos_lista

    carregar_favoritos()

    # ---------- Terço ----------
    terco_estado = {"contador": 0, "indice_misterio": 0}

    def salvar_estado_terco():
        dados = json.dumps(terco_estado)
        try:
            page.client_storage.set("terco_estado", dados)
        except:
            pass
        try:
            page.session.set("terco_estado", dados)
        except:
            pass

    def carregar_estado_terco():
        try:
            dados = page.client_storage.get("terco_estado")
            if dados is None:
                dados = page.session.get("terco_estado")
            if dados:
                estado = json.loads(dados) if isinstance(dados, str) else dados
                terco_estado["contador"] = estado.get("contador", 0)
                terco_estado["indice_misterio"] = estado.get("indice_misterio", 0)
        except:
            pass

    carregar_estado_terco()

    # ---------- Busca ----------
    def buscar_versiculos(palavra):
        resultados = []
        palavra_lower = palavra.lower()
        for livro in biblia_dados:
            for capitulo in livro["capitulos"]:
                for versiculo in capitulo["versiculos"]:
                    if palavra_lower in versiculo["texto"].lower():
                        resultados.append({
                            "livro": livro,
                            "capitulo": capitulo,
                            "numero": versiculo["numero"],
                            "texto": versiculo["texto"],
                            "ref": f"{livro['nome']} {capitulo['numero']}:{versiculo['numero']}"
                        })
        return resultados

    # ---------- Configurações ----------
    tamanho_fonte = 16
    def aplicar_tamanho_fonte(tamanho):
        nonlocal tamanho_fonte
        tamanho_fonte = tamanho
        try:
            page.client_storage.set("tamanho_fonte", str(tamanho))
        except:
            pass
        try:
            page.session.set("tamanho_fonte", str(tamanho))
        except:
            pass

    def obter_tamanho_fonte():
        try:
            tam = page.client_storage.get("tamanho_fonte")
            if tam is None:
                tam = page.session.get("tamanho_fonte")
            if tam:
                return int(tam)
        except:
            pass
        return 16

    # ==================== HOME ====================
    def home():
        page.controls.clear()
        
        cabecalho = ft.Container(
            content=ft.Column([
                ft.Text("🕊️ Lumem", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Sua luz para a vida espiritual", size=18, color=ft.Colors.WHITE),
                ft.Text("🙏 \"A luz brilha nas trevas, e as trevas não a compreenderam.\"", 
                        size=15, color=ft.Colors.WHITE, italic=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            padding=5,
            border_radius=0,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#6C3CE1", "#E53E7B"]
            ),
            margin=0,
            width=page.window_width,
        )

        card_size = 220
        spacing = 15
        grid_width = (card_size * 3) + (spacing * 2)
        grid_height = (card_size * 2) + spacing

        # 🔥 MUDANÇA AQUI: caminhos apontam para /assets/images/
        grid = ft.GridView(
            controls=[
                _criar_card("Bíblia", "Leia e estude", "/biblia", ft.Colors.INDIGO_100, "/assets/images/biblia.jpg"),
                _criar_card("Favoritos", "Versículos salvos", "/favoritos", ft.Colors.AMBER_100, None),
                _criar_card("Liturgia", "Liturgia Diária", "/liturgia", ft.Colors.GREEN_100, "/assets/images/pomba.png"),
                _criar_card("Terço", "Reze o Santo Terço", "/terco", ft.Colors.PURPLE_100, "/assets/images/rosario.png"),
                _criar_card("Orações", "Para todos os momentos", "/oracoes", ft.Colors.BLUE_100, "/assets/images/oracao.png"),
                _criar_card("Config.", "Ajustes do app", "/configuracoes", ft.Colors.GREY_200, None),
            ],
            runs_count=3,
            spacing=spacing,
            run_spacing=spacing,
            padding=0,
            width=grid_width,
            height=grid_height,
        )

        grid_container = ft.Container(
            content=grid,
            alignment=ft.Alignment(0, 0),
            expand=True,
        )

        rodape = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Row([
                    ft.Icon(ft.Icons.CHURCH, size=22, color=ft.Colors.AMBER_700),
                    ft.Text("Desenvolvido por", size=10, color=ft.Colors.GREY_600),
                    ft.Text("Dote Digital", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_700),
                    ft.Icon(ft.Icons.FAVORITE, size=12, color=ft.Colors.RED_400),
                    ft.Icon(ft.Icons.WB_SUNNY, size=22, color=ft.Colors.AMBER_700),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=3),
                ft.Text("© 2026 - Todos os direitos reservados", size=8, color=ft.Colors.GREY_500),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            padding=2,
            width=page.window_width,
        )

        conteudo = ft.Column([
            cabecalho,
            grid_container,
            rodape,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, expand=True)

        page.add(
            ft.Container(
                content=conteudo,
                alignment=ft.Alignment(0, 0),
                padding=0,
                expand=True,
            )
        )
        page.update()

    def _criar_card(titulo, subtitulo, rota, cor_fundo, caminho_imagem=None):
        if caminho_imagem:
            icon = ft.Image(
                src=caminho_imagem,
                width=80,
                height=80,
                fit="contain",
            )
        else:
            emojis = {"Favoritos": "⭐", "Config.": "⚙️"}
            icon = ft.Text(emojis.get(titulo, "📖"), size=50)
        
        return ft.Container(
            content=ft.Column([
                icon,
                ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
                ft.Text(subtitulo, size=12, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
            padding=12,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.BLACK12),
            ink=True,
            on_click=lambda e, r=rota: _navegar_para(r),
            width=220,
            height=220,
            margin=0,
        )

    def _navegar_para(rota):
        if rota == "/biblia":
            mostrar_livros()
        elif rota == "/favoritos":
            mostrar_favoritos()
        elif rota == "/liturgia":
            liturgia()
        elif rota == "/terco":
            terco()
        elif rota == "/oracoes":
            mostrar_oracoes()
        elif rota == "/configuracoes":
            configuracoes()
        else:
            home()

    # ==================== BÍBLIA ====================
    def mostrar_livros():
        page.controls.clear()
        campo_busca = ft.TextField(
            hint_text="🔍 Digite uma palavra para buscar",
            width=300,
            on_submit=lambda e: realizar_busca(campo_busca.value),
            border_radius=25,
            filled=True,
            fill_color=ft.Colors.GREY_100,
            prefix_icon=ft.Icons.SEARCH,
        )
        btn_buscar = ft.IconButton(icon=ft.Icons.SEARCH, icon_size=28, on_click=lambda e: realizar_busca(campo_busca.value))
        
        coluna = ft.Column([
            ft.Container(
                content=ft.Text("📖 Bíblia", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
                margin=8,
            ),
            ft.Row([campo_busca, btn_buscar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=15, color=ft.Colors.GREY_300),
            ft.Text("Escolha um livro:", size=16, weight=ft.FontWeight.W_500),
            ft.GridView(
                controls=[
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.BOOK, size=20, color=ft.Colors.INDIGO_600),
                            ft.Text(livro["nome"], size=11, weight=ft.FontWeight.W_500),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=3),
                        padding=4,
                        bgcolor=ft.Colors.INDIGO_50,
                        border_radius=6,
                        ink=True,
                        on_click=lambda e, l=livro: mostrar_capitulos(l),
                        width=95,
                        height=30,
                    ) for livro in biblia_dados
                ],
                runs_count=6,
                spacing=8,
                run_spacing=8,
                expand=True,
            ),
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e: home()),
                ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], scroll=ft.ScrollMode.AUTO)
        page.add(ft.Container(
            content=coluna,
            padding=15,
            expand=True,
        ))
        page.update()

    def realizar_busca(palavra):
        if not palavra or palavra.strip() == "":
            return
        resultados = buscar_versiculos(palavra.strip())
        page.controls.clear()
        if not resultados:
            coluna = ft.Column([
                ft.Text("🔍 Busca", size=28, weight=ft.FontWeight.BOLD),
                ft.Text(f"Nenhum resultado para '{palavra}'.", size=14, color=ft.Colors.GREY_700),
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e: mostrar_livros()),
                ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, scroll=ft.ScrollMode.AUTO)
            page.add(ft.Container(content=coluna, padding=15, expand=True))
            page.update()
            return
        coluna = ft.Column([
            ft.Text(f"🔍 Resultados para '{palavra}'", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(f"Encontrados {len(resultados)} versículos.", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=10),
        ], scroll=ft.ScrollMode.AUTO)
        for r in resultados[:50]:
            btn = ft.Container(
                content=ft.Text(f"{r['ref']} – {r['texto'][:80]}...", size=13),
                padding=12,
                bgcolor=ft.Colors.INDIGO_50,
                border_radius=8,
                ink=True,
                on_click=lambda e, l=r['livro'], c=r['capitulo']: mostrar_versiculos(l, c),
                margin=4,
            )
            coluna.controls.append(btn)
        coluna.controls.append(ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e: mostrar_livros()),
            ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
        ], alignment=ft.MainAxisAlignment.CENTER))
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    def mostrar_capitulos(livro):
        page.controls.clear()
        coluna = ft.Column([
            ft.Text(f"📖 {livro['nome']}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Text("Escolha o capítulo:", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=8),
            ft.GridView(
                controls=[
                    ft.Container(
                        content=ft.Row([
                            ft.Text("✝️", size=14, color=ft.Colors.AMBER_700),
                            ft.Text(f"{cap['numero']}", size=13, weight=ft.FontWeight.W_500),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
                        padding=4,
                        bgcolor=ft.Colors.AMBER_50,
                        border_radius=6,
                        ink=True,
                        on_click=lambda e, c=cap, l=livro: mostrar_versiculos(l, c),
                        width=75,
                        height=28,
                    ) for cap in livro["capitulos"]
                ],
                runs_count=8,
                spacing=6,
                run_spacing=6,
                expand=True,
            ),
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e: mostrar_livros()),
                ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], scroll=ft.ScrollMode.AUTO)
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    def mostrar_versiculos(livro, capitulo):
        tamanho = obter_tamanho_fonte()
        page.controls.clear()
        coluna = ft.Column([
            ft.Text(f"📖 {livro['nome']} - Capítulo {capitulo['numero']}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Divider(height=8),
        ], scroll=ft.ScrollMode.AUTO)
        
        for v in capitulo["versiculos"]:
            ref = f"{livro['nome']} {capitulo['numero']}:{v['numero']}"
            favorito = eh_favorito(ref)
            
            try:
                nota = page.client_storage.get(f"nota_{ref}") or ""
            except AttributeError:
                nota = ""
            tem_nota = nota != ""
            
            def abrir_anotacao(e, r=ref):
                campo = ft.TextField(
                    label="Sua anotação",
                    value=nota,
                    multiline=True,
                    min_lines=3,
                    max_lines=5,
                    width=350,
                )
                def salvar_anotacao(e):
                    try:
                        page.client_storage.set(f"nota_{r}", campo.value)
                    except AttributeError:
                        pass
                    if page.dialog:
                        page.dialog.open = False
                    page.update()
                    mostrar_versiculos(livro, capitulo)
                dialog = ft.AlertDialog(
                    title=ft.Text(f"📝 Anotação - {r}", weight=ft.FontWeight.BOLD),
                    content=campo,
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo()),
                        ft.TextButton("Salvar", on_click=salvar_anotacao),
                    ],
                )
                page.dialog = dialog
                dialog.open = True
                page.update()
            
            def fechar_dialogo():
                if page.dialog:
                    page.dialog.open = False
                    page.update()
            
            linha = ft.Row([
                ft.Text(f"{v['numero']}. ", weight=ft.FontWeight.BOLD, size=tamanho, color=ft.Colors.INDIGO_700),
                ft.Text(v["texto"], expand=True, selectable=True, size=tamanho, color=ft.Colors.GREY_900),
                ft.IconButton(
                    icon=ft.Icons.FAVORITE if favorito else ft.Icons.FAVORITE_BORDER,
                    icon_color=ft.Colors.RED_400 if favorito else ft.Colors.GREY_400,
                    icon_size=22,
                    on_click=lambda e, r=ref, l=livro, c=capitulo: toggle_favorito(r, l, c)
                ),
                ft.IconButton(
                    icon=ft.Icons.EDIT if tem_nota else ft.Icons.EDIT_OUTLINED,
                    icon_color=ft.Colors.AMBER_700 if tem_nota else ft.Colors.GREY_400,
                    icon_size=22,
                    on_click=abrir_anotacao,
                    tooltip="Anotações" + (" (salva)" if tem_nota else ""),
                ),
            ], alignment=ft.MainAxisAlignment.START)
            coluna.controls.append(linha)
        
        coluna.controls.append(ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e: mostrar_capitulos(livro)),
            ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
        ], alignment=ft.MainAxisAlignment.CENTER))
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    def toggle_favorito(ref, livro, capitulo):
        if eh_favorito(ref):
            remover_favorito(ref)
        else:
            adicionar_favorito(ref)
        mostrar_versiculos(livro, capitulo)

    # ==================== FAVORITOS ====================
    def mostrar_favoritos():
        favs = obter_favoritos()
        page.controls.clear()
        if not favs:
            coluna = ft.Column([
                ft.Text("⭐ Meus Favoritos", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
                ft.Text("Você ainda não tem versículos favoritados.", size=14, color=ft.Colors.GREY_700),
                ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
            page.add(ft.Container(content=coluna, padding=15, expand=True))
            page.update()
            return
        coluna = ft.Column([
            ft.Text("⭐ Meus Favoritos", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Divider(height=10),
        ], scroll=ft.ScrollMode.AUTO)
        for ref in favs:
            try:
                partes = ref.split(" ")
                livro_nome = " ".join(partes[:-1])
                cap_num = int(partes[-1].split(":")[0])
                ver_num = int(partes[-1].split(":")[1])
                livro = next((l for l in biblia_dados if l["nome"] == livro_nome), None)
                if livro:
                    capitulo = next((c for c in livro["capitulos"] if c["numero"] == cap_num), None)
                    if capitulo:
                        versiculo = next((v for v in capitulo["versiculos"] if v["numero"] == ver_num), None)
                        if versiculo:
                            btn = ft.Container(
                                content=ft.Text(f"{ref} – {versiculo['texto'][:80]}...", size=13),
                                padding=12,
                                bgcolor=ft.Colors.AMBER_50,
                                border_radius=8,
                                ink=True,
                                on_click=lambda e, l=livro, c=capitulo: mostrar_versiculos(l, c),
                                margin=4,
                            )
                            coluna.controls.append(btn)
            except Exception:
                continue
        coluna.controls.append(ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()))
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    # ==================== LITURGIA ====================
    LEITURAS_FALLBACK = [
        {
            "titulo": "Liturgia do dia {data}",
            "primeira_leitura": "Leitura do Livro do Profeta Isaías 1,1-10\n\nEscutai a palavra do Senhor, ó chefes de Sodoma; prestai ouvidos à instrução do nosso Deus, ó povo de Gomorra! Convertei-vos e voltai ao Senhor.",
            "salmo": "Salmo 50 - Tende piedade de mim, ó Deus, segundo a vossa misericórdia; apagai as minhas transgressões, segundo a multidão das vossas ternuras.",
            "segunda_leitura": "Leitura da Carta de São Paulo aos Romanos 8,12-25\n\nIrmãos, não somos devedores à carne para vivermos segundo a carne; se, porém, pelo Espírito mortificardes as obras do corpo, vivereis.",
            "evangelho": "Evangelho de Jesus Cristo segundo Lucas 11,1-13\n\nNaquele tempo, Jesus estava rezando num lugar. Quando terminou, um dos seus discípulos pediu-lhe: 'Senhor, ensina-nos a orar'.",
            "reflexao": "Senhor, ensina-nos a orar. A oração é o diálogo do coração com Deus. Que possamos buscar a vontade do Pai."
        },
        {
            "titulo": "Liturgia do dia {data}",
            "primeira_leitura": "Leitura do Livro do Profeta Jeremias 18,1-6\n\nLevanta-te e desce à casa do oleiro, e lá te farei ouvir as minhas palavras. Como o barro na mão do oleiro, assim vós estais na minha mão, ó casa de Israel.",
            "salmo": "Salmo 146 - Louvai ao Senhor, porque é bom cantar ao nosso Deus; porque é suave e agradável louvá-lo.",
            "segunda_leitura": "Leitura da Carta de São Tiago 1,19-27\n\nSabei, meus amados irmãos: todo homem seja pronto para ouvir, tardio para falar e tardio para se irar.",
            "evangelho": "Evangelho de Jesus Cristo segundo Mateus 13,1-23\n\nNaquele dia, Jesus saiu de casa e sentou-se à beira do mar. E reuniu-se muita gente ao redor dele.",
            "reflexao": "A Palavra de Deus é semente que cai em diversos terrenos. Que nosso coração seja terra fértil."
        },
        {
            "titulo": "Liturgia do dia {data}",
            "primeira_leitura": "Leitura do Livro do Profeta Ezequiel 36,16-28\n\nDerramarei sobre vós água pura, e sereis purificados; de todas as vossas imundícies e de todos os vossos ídolos vos purificarei.",
            "salmo": "Salmo 51 - Criai em mim um coração puro, ó Deus, e renovai em mim um espírito reto.",
            "segunda_leitura": "Leitura da Carta de São Paulo aos Romanos 6,1-11\n\nIrmãos, fomos batizados em sua morte, para que, assim como Cristo ressuscitou dos mortos, também nós vivamos uma vida nova.",
            "evangelho": "Evangelho de Jesus Cristo segundo João 3,1-17\n\nDeus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.",
            "reflexao": "O amor de Deus é infinito. Ele nos dá a oportunidade de recomeçar."
        }
    ]

    def liturgia(data=None):
        if data is None:
            data = datetime.now()
        data_str = data.strftime("%Y-%m-%d")
        page.controls.clear()

        liturgia_json = None
        for url in [
            f"https://liturgia.digital/api/liturgia?data={data_str}",
            f"https://api.liturgia.xyz/v1/dia?data={data_str}"
        ]:
            try:
                import requests
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    dados = response.json()
                    if dados and "primeira_leitura" in dados and dados["primeira_leitura"]:
                        liturgia_json = dados
                        break
            except:
                continue

        if liturgia_json is None:
            idx = data.day % len(LEITURAS_FALLBACK)
            fallback = LEITURAS_FALLBACK[idx].copy()
            fallback["titulo"] = fallback["titulo"].format(data=data_str)
            liturgia_json = fallback

        coluna = ft.Column([
            ft.Text("📅 Liturgia Diária", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Text(liturgia_json.get("titulo", f"Liturgia do dia {data_str}"), size=18, weight=ft.FontWeight.W_500),
            ft.Divider(height=8),
            ft.Text(f"📖 Primeira Leitura:", weight=ft.FontWeight.BOLD, size=15),
            ft.Text(liturgia_json.get("primeira_leitura", "Leitura indisponível"), size=14, selectable=True),
            ft.Divider(height=4),
            ft.Text(f"📜 Salmo:", weight=ft.FontWeight.BOLD, size=15),
            ft.Text(liturgia_json.get("salmo", "Salmo indisponível"), size=14, selectable=True),
            ft.Divider(height=4),
            ft.Text(f"📖 Segunda Leitura:", weight=ft.FontWeight.BOLD, size=15),
            ft.Text(liturgia_json.get("segunda_leitura", "Leitura indisponível"), size=14, selectable=True),
            ft.Divider(height=4),
            ft.Text(f"✝️ Evangelho:", weight=ft.FontWeight.BOLD, size=15),
            ft.Text(liturgia_json.get("evangelho", "Evangelho indisponível"), size=14, selectable=True),
            ft.Divider(height=4),
            ft.Text(f"💭 Reflexão:", weight=ft.FontWeight.BOLD, size=15),
            ft.Text(liturgia_json.get("reflexao", "Reflexão indisponível"), size=14, selectable=True),
            ft.Divider(height=15),
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e, d=data: liturgia(d - timedelta(days=1))),
                ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: liturgia(datetime.now())),
                ft.IconButton(icon=ft.Icons.ARROW_FORWARD, icon_size=28, on_click=lambda e, d=data: liturgia(d + timedelta(days=1))),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
        ], scroll=ft.ScrollMode.AUTO)
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    # ==================== TERÇO ====================
    MISTERIOS = {
        "Gozosos": {
            "lista": ["Anunciação", "Visitação", "Nascimento de Jesus", "Apresentação de Jesus no Templo", "Encontro de Jesus no Templo"],
            "descricao": [
                "O Anjo Gabriel anuncia a Maria que ela será a Mãe de Deus.",
                "Maria visita Isabel e João Batista salta de alegria.",
                "Jesus nasce na manjedoura em Belém.",
                "Maria e José apresentam Jesus no Templo.",
                "Jesus é encontrado no Templo entre os doutores."
            ]
        },
        "Dolorosos": {
            "lista": ["Agonia no Getsêmani", "Açoitamento", "Coroa de Espinhos", "Caminho do Calvário", "Cruzificação"],
            "descricao": [
                "Jesus suor de sangue no Monte das Oliveiras.",
                "Jesus é flagelado pelos soldados.",
                "Jesus é coroado com espinhos.",
                "Jesus carrega a cruz até o Calvário.",
                "Jesus é crucificado e morre na cruz."
            ]
        },
        "Gloriosos": {
            "lista": ["Ressurreição", "Ascensão", "Descida do Espírito Santo", "Assunção de Maria", "Coroação de Maria"],
            "descricao": [
                "Jesus ressuscita dos mortos ao terceiro dia.",
                "Jesus sobe ao céu em corpo e alma.",
                "O Espírito Santo desce sobre os apóstolos em Pentecostes.",
                "Maria é assunta ao céu em corpo e alma.",
                "Maria é coroada Rainha do Céu e da Terra."
            ]
        },
        "Luminosos": {
            "lista": ["Batismo de Jesus", "Milagre em Caná", "Anúncio do Reino de Deus", "Transfiguração", "Instituição da Eucaristia"],
            "descricao": [
                "Jesus é batizado por João no rio Jordão.",
                "Jesus transforma água em vinho nas bodas de Caná.",
                "Jesus anuncia a chegada do Reino de Deus.",
                "Jesus se transfigura no Monte Tabor.",
                "Jesus institui a Eucaristia na Última Ceia."
            ]
        }
    }

    def obter_misterio_do_dia():
        dias = {0: "Gozosos", 1: "Dolorosos", 2: "Gloriosos", 3: "Luminosos", 4: "Dolorosos", 5: "Gozosos", 6: "Gloriosos"}
        return dias[datetime.now().weekday()]

    dialogo_atual = None

    def terco():
        nonlocal dialogo_atual
        tipo_misterio = obter_misterio_do_dia()
        dados_misterio = MISTERIOS[tipo_misterio]
        lista_misterios = dados_misterio["lista"]
        descricoes = dados_misterio["descricao"]
        contador = terco_estado["contador"]
        indice = terco_estado["indice_misterio"]

        if contador == 0:
            nome_oracao = "Pai Nosso"
            texto_completo = "Pai Nosso que estais no céu, santificado seja o vosso nome; venha a nós o vosso reino; seja feita a vossa vontade assim na terra como no céu. O pão nosso de cada dia nos dai hoje; perdoai as nossas ofensas, assim como nós perdoamos a quem nos tem ofendido; e não nos deixeis cair em tentação, mas livrai-nos do mal. Amém."
        elif contador % 10 == 0:
            nome_oracao = "Glória ao Pai"
            texto_completo = "Glória ao Pai, ao Filho e ao Espírito Santo. Assim como era no princípio, agora e sempre. Amém."
        else:
            nome_oracao = "Ave Maria"
            texto_completo = "Ave Maria, cheia de graça, o Senhor é convosco; bendita sois vós entre as mulheres, e bendito é o fruto do vosso ventre, Jesus. Santa Maria, Mãe de Deus, rogai por nós pecadores, agora e na hora de nossa morte. Amém."

        misterio_atual = lista_misterios[indice]
        descricao_atual = descricoes[indice]
        page.controls.clear()

        def mostrar_texto_completo(e):
            nonlocal dialogo_atual
            if dialogo_atual is not None and dialogo_atual in page.overlay:
                page.overlay.remove(dialogo_atual)
                dialogo_atual = None

            dialog = ft.Container(
                content=ft.Column([
                    ft.Text(nome_oracao, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
                    ft.Divider(height=10),
                    ft.Text(texto_completo, size=16, selectable=True, color=ft.Colors.GREY_900),
                    ft.Row([
                        ft.TextButton("Fechar", on_click=lambda e: fechar_dialogo())
                    ], alignment=ft.MainAxisAlignment.END),
                ], spacing=10, width=400),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color=ft.Colors.BLACK26),
            )
            page.overlay.append(dialog)
            dialogo_atual = dialog
            page.update()

        def fechar_dialogo():
            nonlocal dialogo_atual
            if dialogo_atual is not None and dialogo_atual in page.overlay:
                page.overlay.remove(dialogo_atual)
                dialogo_atual = None
                page.update()

        coluna = ft.Column([
            ft.Text("🙏 Santo Terço", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Mistérios {tipo_misterio}", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_700),
                    ft.Text(f"{indice+1}º Mistério: {misterio_atual}", size=20, color=ft.Colors.AMBER_800),
                    ft.Text(descricao_atual, size=16, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=18,
                bgcolor=ft.Colors.AMBER_50,
                border_radius=14,
                width=page.window_width - 60,
            ),
            ft.Divider(height=15),
            ft.Text(f"Contagem: {contador} / 50", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_800),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Oração: {nome_oracao}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_800),
                    ft.Button(
                        "Ver texto completo",
                        icon=ft.Icons.INFO,
                        on_click=mostrar_texto_completo,
                        style=ft.ButtonStyle(
                            color=ft.Colors.AMBER_700,
                            bgcolor=ft.Colors.AMBER_50,
                        ),
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=12,
                bgcolor=ft.Colors.GREY_50,
                border_radius=10,
                width=page.window_width - 60,
            ),
            ft.Divider(height=25),
            ft.Row([
                ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, icon_size=45, on_click=lambda e: terco_anterior()),
                ft.IconButton(icon=ft.Icons.REFRESH, icon_size=45, on_click=lambda e: terco_reiniciar()),
                ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_size=45, on_click=lambda e: terco_proximo()),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.IconButton(icon=ft.Icons.HOME, icon_size=32, on_click=lambda e: home()),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, scroll=ft.ScrollMode.AUTO)
        page.add(ft.Container(content=coluna, padding=25, expand=True))
        page.update()

    def terco_proximo():
        contador = terco_estado["contador"] + 1
        indice = terco_estado["indice_misterio"]
        if contador > 50:
            contador = 0
            indice = 0
        else:
            if contador % 10 == 0 and contador != 0:
                indice = (indice + 1) % 5
        terco_estado["contador"] = contador
        terco_estado["indice_misterio"] = indice
        salvar_estado_terco()
        terco()

    def terco_anterior():
        contador = terco_estado["contador"] - 1
        indice = terco_estado["indice_misterio"]
        if contador < 0:
            contador = 0
        else:
            if contador % 10 == 0 and contador != 0:
                indice = (indice - 1) % 5
        terco_estado["contador"] = contador
        terco_estado["indice_misterio"] = indice
        salvar_estado_terco()
        terco()

    def terco_reiniciar():
        terco_estado["contador"] = 0
        terco_estado["indice_misterio"] = 0
        salvar_estado_terco()
        terco()

    # ==================== ORAÇÕES ====================
    def mostrar_oracoes():
        page.controls.clear()
        
        icones_categorias = {
            "Manhã": "🌅",
            "Noite": "🌙",
            "Família": "👪",
            "Saúde": "❤️",
            "Momentos Difíceis": "🙏"
        }
        
        grid_categorias = ft.GridView(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text(icones_categorias.get(categoria, "📖"), size=24, text_align=ft.TextAlign.CENTER),
                        ft.Text(categoria, size=8, weight=ft.FontWeight.W_500, color=ft.Colors.INDIGO_800, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"{len(oracoes_dados[categoria])}", size=6, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, expand=True),
                    padding=4,
                    bgcolor=ft.Colors.AMBER_50,
                    border_radius=6,
                    ink=True,
                    on_click=lambda e, cat=categoria: mostrar_oracoes_categoria(cat),
                    width=55,
                    height=55,
                    alignment=ft.Alignment(0, 0),
                ) for categoria in oracoes_dados
            ],
            runs_count=5,
            spacing=6,
            run_spacing=6,
            expand=True,
        )

        propaganda = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.STARS, size=20, color=ft.Colors.AMBER_700),
                    ft.Text("Dote Digital", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
                    ft.Icon(ft.Icons.STARS, size=20, color=ft.Colors.AMBER_700),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
                ft.Text("Criamos apps que transformam vidas.", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ft.Text("Soluções digitais com propósito e excelência.", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.Icon(ft.Icons.FAVORITE, size=14, color=ft.Colors.RED_400),
                    ft.Text("Feito com ❤️ para o Lumem", size=11, color=ft.Colors.GREY_500),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=3),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            padding=8,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            shadow=ft.BoxShadow(blur_radius=6, spread_radius=1, color=ft.Colors.BLACK12),
            margin=8,
            width=page.window_width - 30,
        )

        coluna = ft.Column([
            ft.Text("🕊️ Orações", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Text("Escolha uma categoria:", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=8),
            grid_categorias,
            propaganda,
            ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
        ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6, expand=True)
        
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    def mostrar_oracoes_categoria(categoria):
        page.controls.clear()
        coluna = ft.Column([
            ft.Text(f"🕊️ {categoria}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Text("Escolha uma oração:", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=8),
        ], scroll=ft.ScrollMode.AUTO)
        
        for oracao in oracoes_dados[categoria]:
            btn = ft.Container(
                content=ft.Row([
                    ft.Text("🕊️", size=16, color=ft.Colors.AMBER_600),
                    ft.Text(oracao["titulo"], size=15, weight=ft.FontWeight.W_500, color=ft.Colors.INDIGO_800),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, size=16, color=ft.Colors.GREY_400),
                ], alignment=ft.MainAxisAlignment.START, spacing=8),
                padding=8,
                bgcolor=ft.Colors.INDIGO_50,
                border_radius=8,
                ink=True,
                on_click=lambda e, o=oracao, cat=categoria: mostrar_oracao_texto(o, cat),
                margin=6,
            )
            coluna.controls.append(btn)
        
        coluna.controls.append(ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e: mostrar_oracoes()),
            ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
        ], alignment=ft.MainAxisAlignment.CENTER))
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    def mostrar_oracao_texto(oracao, categoria):
        tamanho = obter_tamanho_fonte()
        page.controls.clear()
        
        coluna = ft.Column([
            ft.Text(f"🕊️ {oracao['titulo']}", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Divider(height=8),
            ft.Text(oracao["texto"], size=tamanho, selectable=True, color=ft.Colors.GREY_900),
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_size=28, on_click=lambda e: mostrar_oracoes_categoria(categoria)),
                ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, scroll=ft.ScrollMode.AUTO)
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    # ==================== CONFIGURAÇÕES ====================
    def configuracoes():
        page.controls.clear()
        tema_atual = page.theme_mode
        tamanho_atual = obter_tamanho_fonte()

        def alternar_tema(e):
            page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            page.update()
            configuracoes()

        def mudar_tamanho(e):
            novo = int(e.control.value)
            aplicar_tamanho_fonte(novo)
            page.update()

        coluna = ft.Column([
            ft.Text("⚙️ Configurações", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_900),
            ft.Divider(height=15),
            ft.Text("Tema:", size=16, weight=ft.FontWeight.W_500),
            ft.IconButton(
                icon=ft.Icons.BRIGHTNESS_6,
                icon_size=36,
                on_click=alternar_tema,
                tooltip="Alternar tema",
            ),
            ft.Divider(height=15),
            ft.Text("Tamanho da fonte:", size=16, weight=ft.FontWeight.W_500),
            ft.Slider(
                min=12,
                max=24,
                value=float(tamanho_atual),
                divisions=6,
                label="{value}px",
                on_change=mudar_tamanho,
                width=250,
            ),
            ft.IconButton(icon=ft.Icons.HOME, icon_size=28, on_click=lambda e: home()),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12)
        page.add(ft.Container(content=coluna, padding=15, expand=True))
        page.update()

    # ==================== INÍCIO ====================
    home()

ft.run(main)
