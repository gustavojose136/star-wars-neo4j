import os
import sys
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.qa_system import StarWarsDynamicQA
from src.config.settings import Settings

load_dotenv()

app = Flask(__name__)

try:
    Settings.validate()
    qa_system = StarWarsDynamicQA()
    print("✅ Sistema QA inicializado com sucesso")
except Exception as e:
    print(f"❌ Erro ao inicializar: {e}")
    qa_system = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Star Wars Knowledge Graph Chat</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background: #e9ecef;
            color: #333;
            margin-right: auto;
        }
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #dee2e6;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        .form-control {
            flex: 1;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        .form-control:focus {
            border-color: #007bff;
        }
        .btn {
            padding: 12px 25px;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .examples {
            margin-top: 15px;
            font-size: 14px;
            color: #666;
        }
        .examples strong {
            color: #007bff;
        }
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
        }
        .error {
            background: #dc3545;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌟 Star Wars QA Chat</h1>
            <p>Faça perguntas sobre o universo Star Wars!</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message bot-message">
                Olá! Sou seu assistente Star Wars. Faça uma pergunta sobre personagens, naves, planetas ou qualquer coisa do universo Star Wars!
            </div>
        </div>
        
        <div class="input-container">
            <form id="chatForm">
                <div class="input-group">
                    <input type="text" id="questionInput" class="form-control" 
                           placeholder="Digite sua pergunta..." required>
                    <button type="submit" class="btn">Enviar</button>
                </div>
            </form>
            <div class="examples">
                <strong>Exemplos:</strong> "Quem é Luke Skywalker?", "Quantas naves Han Solo pilota?", "Listar personagens"
            </div>
        </div>
    </div>

    <script>
        const chatContainer = document.getElementById('chatContainer');
        const chatForm = document.getElementById('chatForm');
        const questionInput = document.getElementById('questionInput');

        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = message;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function addLoadingMessage() {
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message loading';
            loadingDiv.id = 'loadingMessage';
            loadingDiv.textContent = '🔄 Processando...';
            chatContainer.appendChild(loadingDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function removeLoadingMessage() {
            const loadingMessage = document.getElementById('loadingMessage');
            if (loadingMessage) {
                loadingMessage.remove();
            }
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const question = questionInput.value.trim();
            if (!question) return;

            // Adicionar pergunta do usuário
            addMessage(question, true);
            questionInput.value = '';

            // Mostrar loading
            addLoadingMessage();

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question })
                });

                const data = await response.json();
                
                // Remover loading
                removeLoadingMessage();

                if (data.success) {
                    addMessage(data.answer);
                } else {
                    addMessage(`❌ Erro: ${data.error}`, false);
                }
            } catch (error) {
                removeLoadingMessage();
                addMessage('❌ Erro de conexão. Tente novamente.', false);
            }
        });

        // Focar no input ao carregar
        questionInput.focus();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'success': False, 'error': 'Pergunta vazia'})
        
        if not qa_system:
            return jsonify({'success': False, 'error': 'Sistema QA não inicializado'})
        
        answer = qa_system.ask(question)
        return jsonify({'success': True, 'answer': answer})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🌟 Iniciando servidor web...")
    print("📱 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 