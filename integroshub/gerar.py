# Monta integroshub/index.html: a mesma página de convite de pagamento/, com o cupom INTEGROSHUB (R$ 189,90).
# Uso: python gerar.py   (rode de novo sempre que pagamento/modelo.html mudar)
import pathlib
import sys

PASTA = pathlib.Path(__file__).resolve().parent
ORIGEM = PASTA.parent / "pagamento"
sys.path.insert(0, str(ORIGEM))
from gerar_pagamento import pix, qr_svg, CHAVE  # noqa: E402

VALOR = "189.90"
CARTAO = "https://link.infinitepay.io/ramon-berba-vieira/VC1DLTItSQ-gRvUP3ZZtd-189,90"

TROCAS = [
    ("(WVEIGA ou RBERBA)", "(INTEGROSHUB)"),
    ("<b>R$ 182,00</b>", "<b>R$ 189,90</b>"),
    ("O valor de R$ 182,00 já vem preenchido", "O valor de R$ 189,90 já vem preenchido"),
    ("Em até 2x sem juros de R$ 91,00", "Em até 2x sem juros de R$ 94,95"),
    ('"Pagamento: R$ 182,00 por "', '"Pagamento: R$ 189,90 por "'),
    ('<label><input type="radio" name="cupom" value="WVEIGA"> WVEIGA</label>\n      <label><input type="radio" name="cupom" value="RBERBA"> RBERBA</label>',
     '<label><input type="radio" name="cupom" value="INTEGROSHUB" checked> INTEGROSHUB</label>'),
    ('src="fotos/', 'src="../pagamento/fotos/'),
    ('"hubConviteInicio"', '"hubConviteInicioIntegros"'),
]

if __name__ == "__main__":
    html = (ORIGEM / "modelo.html").read_text(encoding="utf-8")
    for a, b in TROCAS:
        if a not in html:
            sys.exit(f"Trecho não encontrado no modelo: {a[:60]}")
        html = html.replace(a, b)
    codigo = pix(VALOR, "HUB1411INTEGROS")
    chave_fmt = f"{CHAVE[:3]}.{CHAVE[3:6]}.{CHAVE[6:9]}-{CHAVE[9:]}"
    html = html.replace("{{PIX}}", codigo).replace("{{QR}}", qr_svg(codigo)).replace("{{CHAVE_FMT}}", chave_fmt).replace("{{CARTAO}}", CARTAO)
    (PASTA / "index.html").write_text(html, encoding="utf-8")
    print(codigo)
