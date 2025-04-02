from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vídeo Recebido</title>
</head>
<body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
    {% if video %}
        <h1>✅ Vídeo recebido!</h1>
        <p><a href="{{ video }}" target="_blank">🎥 Ver no YouTube</a></p>
    {% else %}
        <h1>❌ Nenhum vídeo foi especificado.</h1>
    {% endif %}
</body>
</html>
"""

@app.route('/youtube')
def youtube():
    video = request.args.get('video')
    return render_template_string(HTML_TEMPLATE, video=video)
