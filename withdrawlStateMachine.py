from statemachine import StateMachine, State
from atm_machine import atm
from DB import state_machine_decorator, db
from functools import wraps

class withdrawlStateMachine(StateMachine):
    # States
    start = State('Start', initial=True)
    amountValidated = State('Validate Amount')
    clientBalanceChecked = State('Check Client Balance')
    withdrawalCalculated = State('Calculate Withdral')
    moneyGiven = State('Give Money')
    atmFundsUpdated = State('Update ATM Funds')
    clientBalanceUpdated = State('Update Client Balance')
    end = State('End', final=True)
    error = State('Error', final=True)

    # Transitions
    startToAmountValidated = start.to(amountValidated)
    amountValidatedToClientBalanceChecked = amountValidated.to(clientBalanceChecked)
    clientBalanceCheckedToWithdrawalCalculated = clientBalanceChecked.to(withdrawalCalculated)
    withdrawalCalculatedToMoneyGiven = withdrawalCalculated.to(moneyGiven)
    moneyGivenToATMFundsUpdated = moneyGiven.to(atmFundsUpdated)
    atmFundsUpdatedToClientBalanceUpdated = atmFundsUpdated.to(clientBalanceUpdated)
    clientBalanceUpdatedToEnd = clientBalanceUpdated.to(end)
    clientBalanceUpdatedToError = clientBalanceUpdated.to(error)
    

    def __init__(self,amount):
        self.amount = amount
        self.state_machine_log_id = db.log_state_machine(type=1, parameters={'amount': amount})
        super(withdrawlStateMachine, self).__init__()

    # Callbacks
    @state_machine_decorator
    def on_startToAmountValidated(self):
        print(f'Validating Amount {self.amount}')
        atm.validate_withdrawl(self.amount)
        return True

    @state_machine_decorator
    def on_amountValidatedToClientBalanceChecked(self):
        print('Checking Client Balance')
        return True

    @state_machine_decorator
    def on_clientBalanceCheckedToWithdrawalCalculated(self):
        print('Calculating Withdrawal')
        withdrawl = atm.calculate_withdrawl(self.amount)
        self.withdrawal_bills = withdrawl
        return True

    @state_machine_decorator
    def on_withdrawalCalculatedToEnd(self):
        return True
    
    @state_machine_decorator
    def on_withdrawalCalculatedToMoneyGiven(self):
        print('Giving Money')
        return True

    @state_machine_decorator
    def on_moneyGivenToATMFundsUpdated(self):
        print('Updating ATM Bills')
        return atm.update_funds(self.withdrawal_bills)
         
    @state_machine_decorator
    def on_atmFundsUpdatedToClientBalanceUpdated(self):
        print('Updating Client Balance')
        return True

    @state_machine_decorator
    def on_clientBalanceUpdatedToEnd(self):
        print('Updating Client Balance')
        print('Ending')
        return self.withdrawal_bills