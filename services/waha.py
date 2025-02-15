import requests

class Waha:

    def __init__(self):
        # URL base da API WAHA
        self.__api_url = 'http://waha:3000'

    def send_message(self, chat_id, message):
        # Endpoint para enviar mensagem
        url = f'{self.__api_url}/api/sendText'

        # Cabeçalhos para a requisição
        headers = {
            'Content-Type': 'application/json',
        }

        # Payload com os dados da mensagem
        payload = {
            'session': 'default',  # Sessão de chat (pode ser customizada)
            'chatId': chat_id,     # ID do chat para envio
            'text': message,       # Mensagem a ser enviada
        }

        # Enviando a requisição POST para a API
        response = requests.post(url=url, json=payload, headers=headers)

        # Checagem de erro (opcional, pode ser adicionado para um comportamento mais robusto)
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem: {response.text}")
        return response  # Retorna a resposta para uso posterior, caso necessário

    def start_typing(self, chat_id):
        url = f'{self.__api_url}/api/startTyping'
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': 'default',
            'chatId': chat_id,
        }
        requests.post(
            url=url,
            json=payload,
            headers=headers,
        )

    def stop_typing(self, chat_id):
        url = f'{self.__api_url}/api/stopTyping'
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': 'default',
            'chatId': chat_id,
        }
        requests.post(
            url=url,
            json=payload,
            headers=headers,
        )

    def get_history_messages(self, chat_id, limit):
        url = f'{self.__api_url}/api/default/chats/{chat_id}/messages?limit={limit}&downloadMedia=false'
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.get(
            url=url,
            headers=headers,
        )
        return response.json()
