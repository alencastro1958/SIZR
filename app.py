from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageFilter
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Dimensões predefinidas para redes sociais
DIMENSOES_REDES = {
    'facebook_post': {'nome': 'Facebook Post', 'dimensoes': (1200, 630)},
    'facebook_cover': {'nome': 'Facebook Cover', 'dimensoes': (820, 312)},
    'instagram_post': {'nome': 'Instagram Post', 'dimensoes': (1080, 1080)},
    'instagram_story': {'nome': 'Instagram Story', 'dimensoes': (1080, 1920)},
    'twitter_post': {'nome': 'Twitter Post', 'dimensoes': (1200, 675)},
    'linkedin_post': {'nome': 'LinkedIn Post', 'dimensoes': (1200, 627)},
    'pinterest_pin': {'nome': 'Pinterest Pin', 'dimensoes': (1000, 1500)},
    'youtube_thumbnail': {'nome': 'YouTube Thumbnail', 'dimensoes': (1280, 720)},
}

# Dimensões para favicons
DIMENSOES_FAVICON = [16, 32, 48, 64, 128, 192]

def redimensionar_imagem(img, largura, altura, manter_aspecto=False):
    """Redimensiona imagem com opção de manter aspecto"""
    if manter_aspecto:
        img.thumbnail((largura, altura), Image.Resampling.LANCZOS)
    else:
        img = img.resize((largura, altura), Image.Resampling.LANCZOS)
    return img

@app.route('/')
def index():
    return render_template('index.html', 
                         redes=DIMENSOES_REDES, 
                         favicons=DIMENSOES_FAVICON)

@app.route('/processar', methods=['POST'])
def processar():
    try:
        if 'imagem' not in request.files:
            return jsonify({'erro': 'Nenhuma imagem selecionada'}), 400
        
        arquivo = request.files['imagem']
        if arquivo.filename == '':
            return jsonify({'erro': 'Arquivo inválido'}), 400
        
        # Carregar imagem
        img_original = Image.open(arquivo)
        formato_original = img_original.format or 'PNG'

        # Obter qualidade desejada
        qualidade = int(request.form.get('qualidade', 90))
        if qualidade < 10 or qualidade > 100:
            qualidade = 90

        # Obter opções do formulário
        acao = request.form.get('acao')
        
        if acao == 'redes_sociais':
            redes_selecionadas = request.form.getlist('redes[]')[:3]  # Limita a 3
            arquivos_zip = io.BytesIO()
            from zipfile import ZipFile
            with ZipFile(arquivos_zip, 'w') as zipf:
                for rede_key in redes_selecionadas:
                    if rede_key in DIMENSOES_REDES:
                        dim = DIMENSOES_REDES[rede_key]['dimensoes']
                        img_processada = redimensionar_imagem(
                            img_original.copy(), dim[0], dim[1]
                        )
                        # Aplica filtro de nitidez
                        img_processada = img_processada.filter(ImageFilter.SHARPEN)
                        buffer = io.BytesIO()
                        if formato_original.upper() == 'JPEG':
                            img_processada.save(buffer, format=formato_original, quality=qualidade)
                        elif formato_original.upper() == 'PNG':
                            # compress_level: 0 (sem compressão) a 9 (máxima compressão)
                            compress_level = max(0, 9 - (qualidade // 11))
                            img_processada.save(buffer, format=formato_original, compress_level=compress_level)
                        else:
                            img_processada.save(buffer, format=formato_original)
                        buffer.seek(0)
                        nome_arquivo = f"{DIMENSOES_REDES[rede_key]['nome'].replace(' ', '_').lower()}_{dim[0]}x{dim[1]}.{formato_original.lower()}"
                        zipf.writestr(nome_arquivo, buffer.read())
            arquivos_zip.seek(0)
            if len(redes_selecionadas) == 1:
                # Se só uma, retorna direto
                with ZipFile(arquivos_zip) as zipf:
                    nome_arquivo = zipf.namelist()[0]
                    buffer = io.BytesIO(zipf.read(nome_arquivo))
                    buffer.seek(0)
                    return send_file(
                        buffer,
                        mimetype=f'image/{formato_original.lower()}',
                        as_attachment=True,
                        download_name=nome_arquivo
                    )
            else:
                return send_file(
                    arquivos_zip,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='imagens_redes_sociais.zip'
                )
        elif acao == 'favicon':
            tamanhos_selecionados = request.form.getlist('favicons[]')[:3]  # Limita a 3
            arquivos_zip = io.BytesIO()
            from zipfile import ZipFile
            with ZipFile(arquivos_zip, 'w') as zipf:
                for tamanho in tamanhos_selecionados:
                    tamanho = int(tamanho)
                    img_favicon = img_original.copy()
                    img_favicon = img_favicon.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
                    # Aplica filtro de nitidez
                    img_favicon = img_favicon.filter(ImageFilter.SHARPEN)
                    buffer = io.BytesIO()
                    # PNG: compress_level de 0 (sem compressão) a 9 (máxima compressão)
                    compress_level = max(0, 9 - (qualidade // 11))
                    img_favicon.save(buffer, format='PNG', compress_level=compress_level)
                    buffer.seek(0)
                    nome_arquivo = f'favicon_{tamanho}x{tamanho}.png'
                    zipf.writestr(nome_arquivo, buffer.read())
            arquivos_zip.seek(0)
            if len(tamanhos_selecionados) == 1:
                with ZipFile(arquivos_zip) as zipf:
                    nome_arquivo = zipf.namelist()[0]
                    buffer = io.BytesIO(zipf.read(nome_arquivo))
                    buffer.seek(0)
                    return send_file(
                        buffer,
                        mimetype='image/png',
                        as_attachment=True,
                        download_name=nome_arquivo
                    )
            else:
                return send_file(
                    arquivos_zip,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='favicons.zip'
                )
        
        elif acao == 'customizado':
            # Conversão de unidade para px (1 cm = 37.8 px em 96 dpi)
            def to_px(valor, unidade):
                try:
                    valor = float(valor)
                except Exception:
                    return 0
                if unidade == 'cm':
                    return int(round(valor * 37.8))
                return int(round(valor))

            largura = to_px(request.form.get('largura_custom', 800), request.form.get('largura_unidade', 'px'))
            altura = to_px(request.form.get('altura_custom', 600), request.form.get('altura_unidade', 'px'))
            manter_aspecto = request.form.get('manter_aspecto') == 'on'
            
            img_custom = redimensionar_imagem(
                img_original.copy(), largura, altura, manter_aspecto
            )
            # Aplica filtro de nitidez
            img_custom = img_custom.filter(ImageFilter.SHARPEN)
            
            buffer = io.BytesIO()
            if formato_original.upper() == 'JPEG':
                img_custom.save(buffer, format=formato_original, quality=qualidade)
            elif formato_original.upper() == 'PNG':
                compress_level = max(0, 9 - (qualidade // 11))
                img_custom.save(buffer, format=formato_original, compress_level=compress_level)
            else:
                img_custom.save(buffer, format=formato_original)
            buffer.seek(0)
            
            return send_file(
                buffer,
                mimetype=f'image/{formato_original.lower()}',
                as_attachment=True,
                download_name=f'custom_{largura}x{altura}.{formato_original.lower()}'
            )
        
        return jsonify({'erro': 'Nenhum processamento realizado'}), 400
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)