<<<<<<< HEAD


# 🖼️ SIZR - Redimensione Imagens em Segundos

<p align="center">
  <img src="static/logo.svg" width="200" alt="Logo Sizr">
</p>

<p align="center">
  <strong>Redimensione imagens para redes sociais e favicons em segundos</strong>
</p>

---

## 🌟 Visão Geral

**Sizr** é um redimensionador de imagens online, rápido e fácil de usar, que gera imagens no tamanho ideal para redes sociais e favicons. Não precisa instalar nada, nem usar ferramentas complexas — basta arrastar, escolher as opções e baixar.

> **"Redimensione em segundos"** — O Sizr transforma seu fluxo de trabalho de minutos para segundos.

---

## ✨ Funcionalidades

### 📱 Pronto para Redes Sociais

Redimensione automaticamente para:

- ✅ Facebook Post (1200x630px)
- ✅ Facebook Cover (820x312px)
- ✅ Instagram Post (1080x1080px)
- ✅ Instagram Story (1080x1920px)
- ✅ Twitter Post (1200x675px)
- ✅ LinkedIn Post (1200x627px)
- ✅ Pinterest Pin (1000x1500px)
- ✅ YouTube Thumbnail (1280x720px)

### ⭐ Gerador de Favicon

Gere vários tamanhos de favicon de uma vez:

- 16x16px, 32x32px, 48x48px, 64x64px, 128x128px, 192x192px

### 🎨 Dimensões Personalizadas

- Defina largura e altura em px ou cm
- Opção para manter proporção
- Redimensionamento de alta qualidade (algoritmo Lanczos + nitidez)

### 🚀 Experiência do Usuário

- Interface Drag & Drop (arraste e solte)
- Visualização em tempo real
- Processamento em lote (até 3 arquivos por vez)
- Não requer cadastro
- 100% gratuito e open source

---

## 📦 Instalação

### Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Local

1. **Clone o repositório:**

```bash
git clone https://github.com/seuusuario/sizr.git
cd sizr
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Execute o aplicativo:**

```bash
python app.py
```

4. **Abra no navegador:**

```
http://127.0.0.1:5000
```

---

## ☁️ Deploy na Internet

Você pode hospedar o Sizr em qualquer plataforma que suporte Python (Heroku, Azure, AWS, VPS, etc). Para produção, use um servidor WSGI como Gunicorn ou Waitress.

Exemplo (Gunicorn):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Para Windows, use Waitress:

```bash
python -m waitress --host=0.0.0.0 --port=5000 app:app
```

Recomenda-se configurar um proxy reverso (Nginx) e HTTPS para produção.

---

## 🤝 Contribua

Contribuições são bem-vindas! Abra issues ou pull requests.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.
=======
# SIZR
**Sizr** é um redimensionador de imagens online, rápido e fácil de usar, que gera imagens no tamanho ideal para redes sociais e favicons. Não precisa instalar nada, nem usar ferramentas complexas — basta arrastar, escolher as opções e baixar.  > **"Redimensione em segundos"** — O Sizr transforma seu fluxo de trabalho de minutos para segundos.
>>>>>>> 66920ada798118c1db45c46015f3cd0add119237
