mongo_user = "akul"
mongo_pass = "NOT4kmZ5hwS4czNa"

mongodb_database = "chatbot"
jwt_secret_key = "12345678"
flask_secret_key = "flask MoC key"
access_token = "12345678"


def get_mongo_url():
    url = "mongodb+srv://" + mongo_user + ":" + mongo_pass + \
        "@cluster0.1zibh.mongodb.net/<dbname>?retryWrites=true&w=majority"
    return url
