from refillStateMachine import refillStateMachine

def refill(money):
    rsm = refillStateMachine()
    if (not rsm.startToMoneyValidated(money)):
        print("Money Not Valid")
        return

    if (not rsm.moneyValidatedToMoneyRecieved()):
        print("Money Not Recieved")
        return
    
    if (not rsm.moneyRecievedToAtmFundsUpdated()):
        print("Not Enought")
        return
    
    if (not rsm.atmFundsUpdatedToEnd()):
        print("Not Enought")
        return
    

    print('Finished Transaction')
