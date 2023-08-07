import mysql.connector
import json
from functools import wraps

def ifnull(var, val):
    if var is None:
        return val
    return var

class DB():
    def __init__(self) -> None:
        self.db_connection = mysql.connector.connect(
                    host="sql7.freesqldatabase.com",
                    user="sql7638042",
                    database="sql7638042",
                    password="JBe3ii6SdF"
                    )
        self.cursor = self.db_connection.cursor(dictionary=True)


    def get_fund_types(self):
        self.cursor.execute("SELECT * FROM fund_types")
        return {float(item['amount']) : item['type'] for item in self.cursor.fetchall()}

    def get_constant_values(self):
        self.cursor.execute("SELECT * FROM constants")
        return {row['name'] :  ifnull(row['value_str'],ifnull(row['value_decimal'],row['value_int'])) for row in self.cursor.fetchall()}
    
    def get_funds(self,atm_id):
        self.cursor.execute(f'SELECT * FROM atm_funds WHERE id = {atm_id}')
        atm_funds = json.loads(self.cursor.fetchone()['funds'])
        return { float(k): v for (k,v) in atm_funds.items()}
    
    def update_funds(self, atm_id, funds):
        funds_to_update = json.dumps(funds)
        query  = "UPDATE atm_funds SET funds=\'%s\' WHERE id = %s" % (funds_to_update,str(atm_id))
        self.cursor.execute(query)
        self.db_connection.commit()
        return True
    
    def update_state_machine_log(self, id, state ,text):
        query = f'UPDATE state_machine_flows SET state=\'{state}\', description=\'{text}\', last_state_time=now() where id={id}'
        self.cursor.execute(query)
        self.db_connection.commit()

    def log_state_machine(self, type, parameters):
        parameters = json.dumps(parameters)
        query = f'insert into state_machine_flows (type, parameters, state, time_started, last_state_time) VALUES({type},\'{parameters}\', \'init\' ,now() ,now())'
        self.cursor.execute(query)
        self.db_connection.commit()
        return self.cursor.lastrowid

db = DB()

def state_machine_decorator(method):
    @wraps(method)
    def inner(self, *method_args, **method_kwargs):
        method_output = method(self, *method_args, **method_kwargs)
        comment = f'Moving from state {self.current_state.id} using method {method.__name__}'
        print(comment)
        db.update_state_machine_log(id = self.state_machine_log_id, state = self.current_state.id, text=comment)
        return method_output
    return inner