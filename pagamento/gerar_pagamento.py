# Monta pagamento/index.html: gera o Pix copia e cola (BR Code estático com valor) e o QR Code em SVG.
# Uso: python gerar_pagamento.py
import io
import pathlib
import qrcode
import qrcode.image.svg

PASTA = pathlib.Path(__file__).resolve().parent
CHAVE = "05193091709"            # CPF do Ramon (chave Pix)
NOME = "RAMON BERBA VIEIRA"
CIDADE = "NITEROI"
VALOR = "182.00"
TXID = "HUB1411"
CARTAO = "https://link.infinitepay.io/ramon-berba-vieira/VC1DLTItSQ-fhODTXWSoA-182,00"
VALOR2 = "311.95"            # 2 ingressos
CARTAO2 = "https://link.infinitepay.io/ramon-berba-vieira/VC1DLTItSQ-lMs5cQunEX-364,00"
VALOR3 = "441.90"            # 3 ingressos
CARTAO3 = "https://link.infinitepay.io/ramon-berba-vieira/VC1DLTItSQ-k0apmj4Yd5-546,00"

def campo(id_, valor):
    return f"{id_}{len(valor):02d}{valor}"

def crc16(dados):
    crc = 0xFFFF
    for b in dados.encode("utf-8"):
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if crc & 0x8000 else (crc << 1)
            crc &= 0xFFFF
    return f"{crc:04X}"

def pix(valor=VALOR, txid=TXID):
    conta = campo("00", "br.gov.bcb.pix") + campo("01", CHAVE)
    corpo = (campo("00", "01") + campo("26", conta) + campo("52", "0000") + campo("53", "986")
             + campo("54", valor) + campo("58", "BR") + campo("59", NOME) + campo("60", CIDADE)
             + campo("62", campo("05", txid)) + "6304")
    return corpo + crc16(corpo)

def qr_svg(texto):
    img = qrcode.make(texto, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO(); img.save(buf)
    svg = buf.getvalue().decode("utf-8")
    return svg[svg.index("<svg"):]

if __name__ == "__main__":
    codigo = pix()
    codigo2 = pix(VALOR2)
    codigo3 = pix(VALOR3)
    chave_fmt = f"{CHAVE[:3]}.{CHAVE[3:6]}.{CHAVE[6:9]}-{CHAVE[9:]}"
    html = (PASTA / "modelo.html").read_text(encoding="utf-8")
    html = html.replace("{{PIX}}", codigo).replace("{{QR}}", qr_svg(codigo)).replace("{{CHAVE_FMT}}", chave_fmt).replace("{{CARTAO}}", CARTAO)
    html = html.replace("{{PIX2}}", codigo2).replace("{{QR2}}", qr_svg(codigo2)).replace("{{CARTAO2}}", CARTAO2)
    html = html.replace("{{PIX3}}", codigo3).replace("{{QR3}}", qr_svg(codigo3)).replace("{{CARTAO3}}", CARTAO3)
    (PASTA / "index.html").write_text(html, encoding="utf-8")
    print(codigo)
