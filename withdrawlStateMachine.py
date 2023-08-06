from statemachine import StateMachine, State
from atm_machine import atm

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
    

    amount = 0
    withdrawal_bills = []
    errors = []

    # Callbacks
    def on_startToAmountValidated(self, amount):
        print('Validating Amount')
        self.amount = amount
        atm.validate_withdrawl(amount)
        return True

    def on_amountValidatedToClientBalanceChecked(self):
        print('Checking Client Balance')
        return True


    def on_clientBalanceCheckedToWithdrawalCalculated(self):
        print('Checking Client Balance')
        withdrawl = atm.calculate_withdrawl(self.amount)
        self.withdrawal_bills = withdrawl
        return True

    def on_withdrawalCalculatedToEnd(self):
        return True
    
    def on_withdrawalCalculatedToMoneyGiven(self):
        print('Giving Money')
        return True

    def on_moneyGivenToATMFundsUpdated(self):
        print('Updating ATM Bills')
        return atm.update_funds(self.withdrawal_bills)
         

    def on_atmFundsUpdatedToClientBalanceUpdated(self):
        print('Updating Client Balance')
        return True

    def on_clientBalanceUpdatedToEnd(self):
        print('Updating Client Balance')
        print('Ending')
        return self.withdrawal_bills