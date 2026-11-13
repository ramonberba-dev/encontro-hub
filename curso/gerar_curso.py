# Monta curso/index.html: pré-venda do curso "O Funcionário Invisível" (Claude para o seu negócio).
# Usa o mesmo estilo da página /especial/ e o mesmo gerador de Pix da /pagamento/.
# Uso: python -B gerar_curso.py
import pathlib, re, sys
PASTA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "pagamento"))
sys.dont_write_bytecode = True
import gerar_pagamento as g

VALOR, TXID = "79.00", "HUBCURSO"

esp = (PASTA.parent / "especial" / "modelo.html").read_text(encoding="utf-8")
claude_svg = re.search(r'(<svg fill="#D97757".*?</svg>)', esp, re.S).group(1)

html = (PASTA / "modelo.html").read_text(encoding="utf-8")
chave_fmt = f"{g.CHAVE[:3]}.{g.CHAVE[3:6]}.{g.CHAVE[6:9]}-{g.CHAVE[9:]}"
codigo = g.pix(VALOR, TXID)
html = (html.replace("{{CLAUDE}}", claude_svg)
            .replace("{{CHAVE_FMT}}", chave_fmt).replace("{{PIX}}", codigo).replace("{{QR}}", g.qr_svg(codigo)))
assert "{{" not in html, "placeholder sobrando"
(PASTA / "index.html").write_text(html, encoding="utf-8")
print("ok")
