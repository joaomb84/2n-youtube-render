from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# Guarda o estado atual do vídeo
video_state = {'url': '', 'status': 'idle', 'updated': False}

@app.route('/youtube_start')
def youtube_start():
    video = request.args.get('video')
    if video:
        video_state['url'] = video
        video_state['status'] = 'playing'
        video_state['updated'] = True
        return f"🎬 Vídeo iniciado: {video}"
    else:
        return "Faltou o link do vídeo", 400

@app.route('/youtube_stop')
def youtube_stop():
    video_state['url'] = ''
    video_state['status'] = 'stopped'
    video_state['updated'] = True
    return "⏹️ Vídeo parado"

@app.route('/viewer')
def viewer():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>2N Viewer</title>
        <script>
            async function checkUpdate() {
                const res = await fetch('/status');
                const data = await res.json();
                const display = document.getElementById('display');
                if (data.updated) {
                    if (data.status === 'playing') {
                        display.innerHTML = `<iframe width="560" height="315"
                          src="${data.url.replace('watch?v=', 'embed/')}"
                          frameborder="0" allowfullscreen></iframe>`;
                    } else if (data.status === 'stopped') {
                        display.innerHTML = '<h2>⏹️ Vídeo parado</h2>';
                    } else {
                        display.innerHTML = '<h2>ℹ️ Botão foi carregado</h2>';
                    }
                }
            }
            setInterval(checkUpdate, 2000);
        </script>
    </head>
    <body style="font-family: sans-serif; text-align: center; margin-top: 80px;">
        <h1>🎬 Aguardando ação do IP Style...</h1>
        <div id="display" style="margin-top: 40px;"></div>
    </body>
    </html>
    '''
    return html

@app.route('/status')
def status():
    global video_state
    data = {
        'url': video_state['url'],
        'status': video_state['status'],
        'updated': video_state['updated']
    }
    video_state['updated'] = False
    return jsonify(data)
