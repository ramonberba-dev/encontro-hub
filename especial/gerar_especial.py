# Monta especial/index.html (cupom HUB50ESPECIAL: 50% em todos os ingressos).
# O modelo sai do pagamento/modelo.html; Pix gerado com o mesmo gerador.
# Uso: python gerar_especial.py
import pathlib, sys
PASTA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "pagamento"))
sys.dont_write_bytecode = True
import gerar_pagamento as g

VALORES = {"": "129.95", "2": "259.90", "3": "389.85"}
TXID = "HUB50ESP"

html = (PASTA / "modelo.html").read_text(encoding="utf-8")
chave_fmt = f"{g.CHAVE[:3]}.{g.CHAVE[3:6]}.{g.CHAVE[6:9]}-{g.CHAVE[9:]}"
html = html.replace("{{CHAVE_FMT}}", chave_fmt)
for suf, v in VALORES.items():
    c = g.pix(v, TXID)
    html = html.replace("{{PIX%s}}" % suf, c).replace("{{QR%s}}" % suf, g.qr_svg(c))
assert "{{" not in html, "placeholder sobrando"
(PASTA / "index.html").write_text(html, encoding="utf-8")
print("ok")
