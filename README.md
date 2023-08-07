# Ronen Dotan - ATM Assignment


URL:https://frozen-fjord-21742-ed9360497415.herokuapp.com/ 

## DB: 
    Host: sql7.freesqldatabase.com

    Database name: sql7638042 

    Database user: sql7638042 

    Database password: JBe3ii6SdF 
    
    Port number: 3306 

app.py is the router of the request.
there are two handlers - **refill_handler** and **withdrawl_handler**, each of which activate the designated state machine.

I've added several states and transition in the state machines - for example, withdrawal:
1. "check client balance", 
2. "give money"
3. "updateATMFunds"
4. "Client balance updated".

**These were added in case this would need to be exctended to be used for the atm and perform all the process, not just calculating the funds.**
Using a state machine will help us be fault tolerent and recover from errors, so if an error occured, the state machine logged all the data and the current state we are at, so in the future we will implement the recovery. For now all is prepared and logged into the DB. Each "withdrawl" or "refill" is loged and the status changges are also logged so recovery is easy.

env_variables.py file, we recieve variable including the atm_id - each atm will have something diffrent, because i've implemented a shared DB between many instances of an atm. it will be recieved from the enviroment variables.

DB.py is an implementation using mySQL, it an be replaced with a diffrent db.

notice the **state_machine_decorator** - which help us log all the transitions of the state machine.

### atm_machine.py
the main class.
This solution is initilaize from the DB.

**calculate_withdrawal** function:
calcualting the withdrawl. 
this problem might be more complex than it seems!

For example, if we have these bills - without limitation:

| bill      | amount |
| ----------- | ----------- |
| 50      | 100       |
| 20   | 100        |
| 10   | 100        |

the limitation is that the amount of coins should be <= 10 - (not 50  - his is a constant and can change)
the withdrawl amount is 62.
So using the basic algorithm we wold give 50, 1,1,1,1,1,1,1,1,1,1,1,1
Now - the amount of coins is > 10! so basically we would finish here and say - we can't handle this with the basic algo.

There is a better solution!

we can give 20,20,20,1,1 - and we are good to go!

So this means that just  removing by amount from top to buttom is not good enought.
I've created a recursion that will calculate several options to the withdrawal amount.This way we will not give an error when in fact we can give the money.
the recursion is working as פונקציה יוצרת, so basically it calculate the next step (bill to give) and continues, untill finishes the amount. it will supply with maximum of 3 valid results. (can be changed)

These results are than prioritize using: prioritize_withdrawl_option, which can accept a dictionary of diffrent weights for each bill and change the withdrawl option.

The default weight:
```{200: 200x200, 100: 100x100, 50: 50x50, 20: 20x20, 10: 10x10, 5:5x5, 1: 1, 0.1: 0.1, 0.01:0.01}```
Will prefer to give big bills first, coins at the end, but will always try to giv result if possible.

notice that MAX_COINS, MAX_WITHDRAWAL_AMOUNT are constant.

Regarding the DB:
to import - look at atm.sql in this repository.

## tables:

**atm_funds** - the current funds for all the atms, seperated by atm_id. the funds are in a json text.

**constants** - to be used in the system, for example MAX_WITHDRAWAL_AMOUNT, MAX_COINS

**fund_types** - all posible funds and clasification to type - bill/ coin

**state_machine_flows** - a log of all the actions done in the system and the transitions.

### state_machine_flows:
each transaction (withdrawal/ refill) is registered, and then on each transition (clientBalanceChecked, withdrawal calculated.... ) the DB is updated so we will know exactly what happened and nothing will get lost.
I am logging the source state and the transition, and time. FFU - to build a script that an restore the action from the state machine in the middle.

Thank You!!!