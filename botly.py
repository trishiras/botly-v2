from core.logging import logger
from langchain_ollama import ChatOllama
from gradio import Chatbot, Textbox, ChatInterface
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class Botly:
    def __init__(self):
        """
        Initialize the Botly class. This method will set default values for
        all class attributes and call the run method to start the bot.

        Attributes:
            llm (None): The language model to use.
            cache (bool): Whether or not to cache the responses.
            verbose (bool): Whether or not to print all messages.
            keep_alive (int): The time to keep the connection alive in seconds.
            diverse_text (float): The percentage of diverse text to generate.
            diversety_index (int): The index of the diverse text.
            creativity_index (float): The creativity index of the generated text.
            tokens_to_generate (int): The number of tokens to generate.
            llm_model (str): The model of the language model to use.
            base_url (str): The URL of the server.
            messages (list): The list of messages to send.
            prompt (str): The prompt to use.
            chain (None): The chain to use.
        """

        self.llm = None
        self.cache = False
        self.verbose = False
        self.keep_alive = 300
        self.diverse_text = 0.9
        self.diversety_index = 40
        self.creativity_index = 0.8
        self.tokens_to_generate = 256
        self.llm_model = "qwen2.5:1.5b"
        self.base_url = "http://localhost:11434"
        self.messages = []
        self.prompt = None
        self.chain = None
        self.run()

    def initialize_ollama(self):
        """
        Initialize the llm model.

        This method will create a new instance of the ChatOllama class
        and set it as the llm attribute of the class.

        """

        ## llm model initialization
        self.llm = ChatOllama(
            model=self.llm_model,
            top_k=self.diversety_index,
            top_p=self.diverse_text,
            cache=self.cache,
            verbose=self.verbose,
            keep_alive=self.keep_alive,
            temperature=self.creativity_index,
            num_predict=self.tokens_to_generate,
            base_url=self.base_url,
        )

    def prompt_generator(self):
        """
        Generate the prompt template for the language model.

        This method sets up the initial messages for the ChatPromptTemplate,
        which serves as the conversation context. The system message defines
        the assistant's behavior, while the user message is a placeholder for
        user input.

        """

        ## prompt template instructions
        logger.info("Adding prompt template instructions...")
        self.messages = [
            (
                "system",
                "You are a helpful assistant. Always answer as short as possible.",
            ),
            ("user", "{input_message}"),
        ]

        ## prompt
        logger.info("Creating prompt template...")
        self.prompt = ChatPromptTemplate.from_messages(self.messages)

    def lang_chain_generator(self):
        """
        Initialize the LangChain chain.

        This method takes the prompt template and language model and chains
        them together to form the LangChain pipeline. The RunnablePassthrough
        node assigns the user's input to a variable called "input_message",
        which is then passed to the prompt template. The output of the
        prompt template is then passed to the language model, and the output
        of the language model is then passed to the StrOutputParser.

        """

        ## chain initialization
        self.chain = (
            RunnablePassthrough.assign(
                input_message=lambda input_dict: input_dict["context"],
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def botly_ui_interface(self):
        """
        Set up the Gradio interface for the chatbot.

        This method uses the `ChatInterface` class from Gradio to create a
        chat interface for the bot. The `ui_responder` function is used to
        generate responses based on the user's input. The interface is
        launched with the `launch` method.

        """

        ## gradio interface
        def ui_responder(
            question,
            history,
        ):
            response = self.chain.invoke(
                {
                    "context": question,
                }
            )
            return response

        ChatInterface(
            ui_responder,
            chatbot=Chatbot(height=500),
            textbox=Textbox(
                placeholder="Hi, I'm Botly! your personal chatbot.",
                container=False,
                scale=7,
            ),
            title="Botly V2",
            examples=[
                "Bonjour",
                "Hello",
                "Namaste",
            ],
        ).launch(share=True)

    def run(self):
        """
        Initialize and run the bot.

        This method initializes the Ollama model, the prompt template, the
        LangChain pipeline, and the Gradio interface. It then launches the
        interface with the `launch` method.

        """

        ## initialize ollama
        logger.info("Botly V2 is initializing...")
        logger.info("Initializing Ollama...")
        self.initialize_ollama()

        ## prompt template
        logger.info("Initializing prompt template...")
        self.prompt_generator()

        ## langchain creation
        logger.info("Initializing LangChain...")
        self.lang_chain_generator()

        ## gradio interface
        logger.info("Initializing Gradio UI...")
        logger.info("Botly V2 is running...")
        self.botly_ui_interface()


if __name__ == "__main__":
    Botly()
    logger.info("Botly V2 is Stopping...")
