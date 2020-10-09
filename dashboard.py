from dao import Executionary
import bcrypt
from config import systemConfig


class Dashboard:
    def __init__(self):
        self.executionar = Executionary.Executionary()

    def create_error_msg(self, msg):
        error_response = {
            "status": "error",
            "message": msg,
            "response": []
        }
        return error_response

    def create_success_response(self, data, msg="data fetched"):
        success_response = {
            "status": "success",
            "response": data,
            "message": msg
        }
        return success_response

    def auth_request(self, input):
        secret_key = systemConfig.jwt_secret_key
        try:
            decode_data = jwt.decode(
                input['jwt_token'], secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            status = 'JWT Token Expired'
        except jwt.InvalidTokenError:
            status = 'Invalid JWT Token'
        except KeyError:
            status = str("JWT token missing")
        except Exception as e:
            status = str(e)
        else:
            user_id = decode_data['username']
            session_id = decode_data['password']
            user_data = self.auth_user(decode_data)
            if user_data["status"] == "success" and user_data["message"] == "Login successful":
                status = 'success'
            else:
                status = 'Invalid user'
        return status

    def auth_user(self, input):
        try:
            user = input["username"]
            passw = input["password"]

            if type(user) != str or type(passw) != str:
                raise TypeError
            if user == "" or passw == "":
                raise ValueError

        except TypeError:
            response = self.create_error_msg("Invalid Data Type")

        except KeyError:
            response = self.create_error_msg("Key not passed")

        except ValueError:
            response = self.create_error_msg("Invalid input")

        except Exception as e:
            response = self.create_error_msg(str(e))
        else:
            try:
                login_user = self.executionar.get_all_data(
                    "users", {'username': user})[0]
            except Exception as e:
                response = self.create_error_msg("User doesn't exists")

            else:
                if "username" in login_user and "password" in login_user:
                    if bcrypt.checkpw(passw.encode('utf-8'), login_user['password']):
                        response = self.create_success_response(
                            [], msg="Login successful")
                    else:
                        response = self.create_error_msg("Invalid Password")
                else:
                    response = self.create_error_msg(
                        "Error in user entry in Database")
        return response

    def register_user(self, input):
        try:
            user = input["username"]
            passw = input["password"]

            if type(user) != str:
                raise TypeError
            if user == "":
                raise ValueError

        except TypeError:
            response = self.create_error_msg("Invalid Data Type")

        except KeyError:
            response = self.create_error_msg("Key not passed")

        except ValueError:
            response = self.create_error_msg("Invalid input")

        except Exception as e:
            response = self.create_error_msg(str(e))
        else:
            data = self.auth_user(input)
            if data["status"] == "success" and data["message"] == "Login successful":
                response = self.create_error_msg("User already exists")

            elif data["status"] == "error" and data["message"] == "User doesn't exists":
                hashpass = bcrypt.hashpw(
                    passw.encode('utf-8'), bcrypt.gensalt())
                try:
                    user_data = {"username": user, "password": hashpass}
                    self.executionar.insert_data("users", user_data)
                except Exception as e:
                    response = self.create_error_msg(str(e))
                else:
                    response = self.create_success_response(
                        [], msg="user added successfully")
        return response

    def add_query(self, input):
        try:
            query = input["query"]
            remark = input["remark"]

            if type(remark) != str or type(query) != str:
                raise TypeError
            if remark == "" or query == "":
                raise ValueError

        except TypeError:
            response = self.create_error_msg("Invalid Data Type")

        except KeyError:
            response = self.create_error_msg("Key not passed")

        except ValueError:
            response = self.create_error_msg("Invalid input")

        except Exception as e:
            response = self.create_error_msg(str(e))
        else:
            try:
                data = {"query": query, "remark": remark}
                self.executionar.insert_data("queries", data)
            except Exception as e:
                response = self.create_error_msg(str(e))
            else:
                response = self.create_success_response(
                    [], msg="query added successfully")
        return response

    def delete_query(self, input):
        try:
            query_id = input["query_id"]

            if type(query_id) != str:
                raise TypeError
            if query_id == "":
                raise ValueError

        except TypeError:
            response = self.create_error_msg("Invalid Data Type")

        except KeyError:
            response = self.create_error_msg("Key not passed")

        except ValueError:
            response = self.create_error_msg("Invalid input")

        except Exception as e:
            response = self.create_error_msg(str(e))
        else:
            try:
                self.executionar.remove_data("queries", "query_id", query_id)
            except Exception as e:
                response = self.create_error_msg(str(e))
            else:
                response = self.create_success_response(
                    [], msg="query deleted successfully")
        return response

    def list_query(self):
        try:
            data = self.executionar.get_all_data("queries")
        except Exception as e:
            response = self.create_error_msg(str(e))
        else:
            response = self.create_success_response(data)
        return response
