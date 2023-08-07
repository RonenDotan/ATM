from statemachine import StateMachine, State
from atm_machine import atm
from DB import state_machine_decorator, db

class refillStateMachine(StateMachine):
    # States
    start = State('Start', initial=True)
    moneyValidated = State()
    moneyRecieved = State()
    atmFundsUpdated = State()
    end = State('End')

    # Transitions
    startToMoneyValidated = start.to(moneyValidated)
    moneyValidatedToMoneyRecieved = moneyValidated.to(moneyRecieved)
    moneyRecievedToAtmFundsUpdated = moneyRecieved.to(atmFundsUpdated)
    atmFundsUpdatedToEnd = atmFundsUpdated.to(end)

    def __init__(self,money):
        self.money = money
        self.state_machine_log_id = db.log_state_machine(type=2, parameters={'money': money})
        super(refillStateMachine, self).__init__()

    # Callbacks
    @state_machine_decorator
    def on_startToMoneyValidated(self):
        print('Validating Money')
        return atm.validate_funds(self.money)

    @state_machine_decorator
    def on_moneyValidatedToMoneyRecieved(self):
        print('Money Recieved From Cashier')
        return True

    @state_machine_decorator
    def on_moneyRecievedToAtmFundsUpdated(self):
        atm.update_funds(self.money, "refill")
        return True
    
    @state_machine_decorator
    def on_atmFundsUpdatedToEnd(self):
        print("Transaction Ended Successfully")
        return True