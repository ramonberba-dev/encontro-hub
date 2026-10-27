# Monta comprar/index.html: Pix copia e cola e QR para o valor cheio e com cupom, e os links do cartão.
# Uso: python gerar_comprar.py   (preencha CARTAO_* quando o Ramon mandar os links da InfinitePay)
import pathlib
import sys

PASTA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA.parent / "pagamento"))
from gerar_pagamento import pix, qr_svg, CHAVE  # noqa: E402

CHEIO, CUPOM = "259.90", "189.90"
CARTAO_CHEIO = "https://link.infinitepay.io/ramon-berba-vieira/VC1DLTItSQ-FYFvhSyvI0-259,90"   # link InfinitePay de R$ 259,90
CARTAO_CUPOM = "https://link.infinitepay.io/ramon-berba-vieira/VC1DLTItSQ-gRvUP3ZZtd-189,90"   # link InfinitePay de R$ 189,90
PARCELA_CHEIO = ""  # ex.: "Em até 2x sem juros de R$ 129,95" (só se o link permitir)
PARCELA_CUPOM = ""  # ex.: "Em até 2x sem juros de R$ 94,95"

if __name__ == "__main__":
    pix_cheio, pix_cupom = pix(CHEIO, "HUB1411CHEIO"), pix(CUPOM, "HUB1411CUPOM")
    chave_fmt = f"{CHAVE[:3]}.{CHAVE[3:6]}.{CHAVE[6:9]}-{CHAVE[9:]}"
    trocas = {
        "{{PIX_CHEIO}}": pix_cheio, "{{PIX_CUPOM}}": pix_cupom,
        "{{QR_CHEIO}}": qr_svg(pix_cheio), "{{QR_CUPOM}}": qr_svg(pix_cupom),
        "{{CHAVE_FMT}}": chave_fmt,
        "{{CARTAO_CHEIO}}": CARTAO_CHEIO, "{{CARTAO_CUPOM}}": CARTAO_CUPOM,
        "{{PARCELA_CHEIO}}": PARCELA_CHEIO, "{{PARCELA_CUPOM}}": PARCELA_CUPOM,
        "{{PARCELA_TXT}}": PARCELA_CHEIO, "{{PARCELA_HIDDEN}}": "" if PARCELA_CHEIO else " hidden",
    }
    html = (PASTA / "modelo.html").read_text(encoding="utf-8")
    for k, v in trocas.items():
        html = html.replace(k, v)
    (PASTA / "index.html").write_text(html, encoding="utf-8")
    print(pix_cheio); print(pix_cupom)
