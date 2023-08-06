from withdrawlStateMachine import withdrawlStateMachine


def withdraw(amount):
    try:
        wsm = withdrawlStateMachine()
        if (not wsm.startToAmountValidated(amount)):
            pass

        if (not wsm.amountValidatedToClientBalanceChecked(amount)):
            pass

        if (not wsm.clientBalanceCheckedToWithdrawalCalculated()):
            pass

        if (not wsm.withdrawalCalculatedToMoneyGiven()):
            pass

        if (not wsm.moneyGivenToATMFundsUpdated()):
            pass
        
        if (not wsm.atmFundsUpdatedToClientBalanceUpdated()):
            pass

        result = wsm.clientBalanceUpdatedToEnd()
        if (not result):
            print("Not Enought")
            return False
        else:
            return result
    except Exception as e:
        print(e)
        raise e
    
     

#wsm.current_state = State('Error', id='error', value='error', final=True)
    
