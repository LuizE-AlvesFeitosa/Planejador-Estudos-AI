from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# 🔑 COLE SUA CHAVE DA GROQ AQUI!
CHAVE_GROQ = "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"

# Inicializa o cliente da Groq
cliente = Groq(api_key=CHAVE_GROQ)

# Defina o modelo que você quer usar (você pode trocar se quiser)
# Lista de modelos disponíveis: https://console.groq.com/docs/models
MODELO = "llama-3.3-70b-versatile"  # Um modelo muito capaz e rápido [citation:5][citation:7]

@app.route('/gerar-plano', methods=['POST'])
def gerar_plano():
    try:
        dados = request.json

        prova = dados.get('prova', '')
        materias = dados.get('materias', '')
        dias = dados.get('dias', '')
        horas = dados.get('horas', '')
        nivel = dados.get('nivel', 'Iniciante')

        # Monta o prompt para o modelo (igual ao que você usava)
        prompt = f"""
        Você é um professor especialista em criar planos de estudo.

        PROVA: {prova}
        MATÉRIAS: {materias}
        DIAS DISPONÍVEIS: {dias} dias
        HORAS POR DIA: {horas} horas
        NÍVEL DO ALUNO: {nivel}

        Crie um plano de estudos DIA A DIA, organizado e fácil de seguir.
        """

        # Faz a chamada para a API da Groq [citation:1][citation:9]
        resposta = cliente.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODELO,
            temperature=0.7,  # Controla a criatividade (0 = mais preciso, 1 = mais criativo)
            max_tokens=1024,   # Limite de tamanho da resposta
        )

        plano_gerado = resposta.choices[0].message.content

        return jsonify({
            'sucesso': True,
            'plano': plano_gerado
        })

    except Exception as erro:
        # Se houver algum erro na chamada da API, ele vai aparecer aqui
        return jsonify({
            'sucesso': False,
            'erro': str(erro)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)