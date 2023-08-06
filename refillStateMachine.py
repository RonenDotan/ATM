from statemachine import StateMachine, State
from atm_machine import atm


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

    money = {}

    # Callbacks
    def on_startToMoneyValidated(self, money):
        print('Validating Money')
        self.money = money
        return atm.validate_funds(money)

    
    def on_moneyValidatedToMoneyRecieved(self):
        print('Money Recieved From Cashier')
        return True

    def on_moneyRecievedToAtmFundsUpdated(self):
        atm.update_funds(self.money, "refill")
        return True
    
    def on_atmFundsUpdatedToEnd(self):
        print("Transaction Ended Successfully")
        return True