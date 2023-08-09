from refillStateMachine import refillStateMachine

def refill(money):
    rsm = refillStateMachine(money)
    if (not rsm.startToMoneyValidated()):
        return

    if (not rsm.moneyValidatedToMoneyRecieved()):
        return
    
    if (not rsm.moneyRecievedToAtmFundsUpdated()):
        return
    
    if (not rsm.atmFundsUpdatedToEnd()):
        return
    
    
    print('Finished Transaction')
    
