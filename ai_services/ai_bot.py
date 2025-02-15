import os
from decouple import config
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')

class AIBot:
    """
    AIBot is a virtual assistant for a barbershop, designed to interact with customers via WhatsApp. 
    It can answer general questions about the barbershop and manage appointment scheduling by accessing 
    a local spreadsheet and relevant barbershop information (RAG).
    """

    def __init__(self):
        """
        Initializes the AIBot with a chat model and a retriever.
        """
        self.__chat = ChatGroq(model='deepseek-r1-distill-llama-70b', temperature=0.2)
        self.__retriever = self.__build_retriever()

    def __build_retriever(self):
        """
        Builds and returns a retriever for fetching relevant documents.
        """
        persist_directory = '/app/chroma_data'
        embedding = HuggingFaceEmbeddings()
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding,
        )
        return vector_store.as_retriever(search_kwargs={'k': 30})

    def __build_messages(self, history_messages, question):
        messages = []
        for message in history_messages:
            message_class = HumanMessage if message.get('fromMe') else AIMessage
            messages.append(message_class(content=message.get('body')))
        messages.append(HumanMessage(content=question))
        return messages

    def invoke(self, history_messages, question):
        SYSTEM_TEMPLATE = '''
        You are a virtual assistant for a barbershop, specialized in assisting customers via WhatsApp. Your main role is to provide quick, polite, and helpful answers based on the available information document.

        Instructions:

        - Respond in a polite, light, and relaxed manner, always maintaining a natural and friendly tone.
        - Always be empathetic and proactive in your responses, even when you don’t know the exact answer.
        - If you don’t know the answer, politely apologize and, if possible, offer to help find a solution.
        - Do not ask invasive questions about customers' personal matters. Focus solely on answering questions about the barbershop’s services.
        
        General Rules:

        - Always communicate in Portuguese (PT-BR).
        - Be clear and objective, always providing the best possible experience for the customer.
        - Maintain a relaxed and friendly tone, as if you were talking to a friend.
        - If you have doubts or don’t know the answer, politely say you don’t know.
        
        Example of Interaction:

        Q: Oi, a barbearia está aberta?  
        A: E aí, tranquilo? Estamos abertos sim! Funcionamos de segunda a sábado, das 7h às 20h. Se precisar de mais alguma coisa, estou por aqui!

        Q: {Question}
        A: 
        '''
        SYSTEM_TEMPLATE = SYSTEM_TEMPLATE.format(Question=question)
        
        # Retrieve relevant documents based on the question
        docs = self.__retriever.invoke(question)

        # Create a prompt template for the chat model
        question_answering_prompt = ChatPromptTemplate.from_messages(
            [
            ('system', SYSTEM_TEMPLATE),
            MessagesPlaceholder(variable_name='messages'),
            ]
        )

        # Create a document chain for processing the documents with the chat model
        document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt)

        # Invoke the document chain with the context and messages
        response = document_chain.invoke(
            {
            'context': docs,
            'messages': self.__build_messages(history_messages, question),
            }
        )

        return response

