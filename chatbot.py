from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
from dao import Executionary


class MoC_Chatbot:
    def __init__(self):
        self.chatbot = ChatBot('MoC_bot', storage_adapter='chatterbot.storage.SQLStorageAdapter',
                               logic_adapters=[
                                   {
                                       'import_path': 'chatterbot.logic.BestMatch',
                                       'default_response': "I am sorry, couldn't get your query.<br><br>You can call us on 011-29581223, 1239, 1241 <br><br> You can also mail us at <br>1. iic.mhrd@aicte-india.org <br>2. innovationofficer2@aicte-india.org",
                                       'maximum_similarity_threshold': 0.90
                                   }
                               ],
                               database_uri='sqlite:///database.sqlite3'
                               )
        self.executionar = Executionary.Executionary()
        self.train_bot()

    def train_bot(self):
        data = json.load(open('training_data/queries.json'))
        unstruct_mongo_queries = self.executionar.get_all_data("queries")
        struct_mongo_queries = []
        for query in unstruct_mongo_queries:
            struct_mongo_queries.append([query["query"], query["remark"]])

        total_queries = data["real_queries"] + \
            data["custom_queries"] + struct_mongo_queries

        trainer = ListTrainer(self.chatbot, show_training_progress=False)
        for ele in total_queries:
            trainer.train(ele)

        # Training with English Corpus Data
        trainer_corpus = ChatterBotCorpusTrainer(
            self.chatbot, show_training_progress=False)
        trainer_corpus.train(
            "chatterbot.corpus.english.greetings",
            "chatterbot.corpus.english.conversations"
        )
