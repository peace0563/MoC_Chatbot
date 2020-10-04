from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import json

# Creating ChatBot Instance
chatbot = ChatBot(
    'micbot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': "I am sorry, couldn't get your query.<br><br>You can call us on 011-29581223, 1239, 1241 <br><br> You can also mail us at <br>1. iic.mhrd@aicte-india.org <br>2. innovationofficer2@aicte-india.org",
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

data = json.load(open('training_data/queries.json'))
total_queries = data["real_queries"] + data["custom_queries"]

trainer = ListTrainer(chatbot, show_training_progress=False)
for ele in total_queries:
    trainer.train(ele)

# Training with English Corpus Data
trainer_corpus = ChatterBotCorpusTrainer(chatbot, show_training_progress=False)
trainer_corpus.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations"
)
