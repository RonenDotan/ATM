MAX_COINS = 10
FUND_TYPES = {200: 'BILL', 
              100: 'BILL', 
              50: 'BILL', 
              20: 'BILL', 
              10: 'COIN',
              5: 'COIN',
              1: 'COIN', 
              0.1: 'COIN', 
              0.01: 'COIN'}
MAX_WITHDRAWAL_AMOUNT = 2000
from collections import Counter
from functools import reduce


class UnprocessableEntity(Exception):
    message = "UnprocessableEntity"
    status_code = 422

class conflict(Exception):
    message = "conflict"
    status_code = 409


class ATMMachine:
    def __init__(self, initial_funds):
        self.funds = initial_funds

    def calculate_withdrawl(self, amount):
        withdrawl_options = []
        solution_without_coins_limit = False

        def internal_withdrawl_calculation(amount, atm_content, output, total_coins):
            nonlocal solution_without_coins_limit
            if len(withdrawl_options) > 10:
                return
            for curr_bill, bill_amount in atm_content.items():
                if bill_amount == 0:
                    continue

                if self.is_coin(curr_bill):
                    total_coins += 1
                    if total_coins > MAX_COINS:
                        if solution_without_coins_limit:
                            return

                if curr_bill == amount:
                    if total_coins > MAX_COINS:
                        solution_without_coins_limit = True
                        return
                    else:
                        withdrawl_options.append(output + [curr_bill])
                        return
                elif curr_bill < amount:
                    tmp = {k: v for k, v in atm_content.items() if k <= curr_bill}
                    tmp[curr_bill] -= 1
                    internal_withdrawl_calculation(amount - curr_bill, tmp, output + [curr_bill], total_coins)

        internal_withdrawl_calculation(amount=amount,atm_content=self.funds, output=[], total_coins=0)
        return self.prioritize_withdrawl_option(withdrawl_options = withdrawl_options, solution_without_coins_limit = solution_without_coins_limit)
    
    def prioritize_withdrawl_option(self, withdrawl_options, solution_without_coins_limit ,priority_weight = {50: 500000, 20: 2000, 1: 0}):
        # We can use this to prioritzie the withdrawl options - for now, just summing up and selecting the first one
        result = []
        if len(withdrawl_options) == 0: # We couldn't find a way to fullfill the request - not enouth money in ATM
            if solution_without_coins_limit:
                raise UnprocessableEntity
            else:
                raise conflict
            

        for withdrawl_option in withdrawl_options:
            result_summarize = dict(Counter(withdrawl_option))
            sum_pririty = 0
            for bill, amount in result_summarize.items():
                sum_pririty += amount * priority_weight.setdefault(bill,0)
            result.append({"result" : result_summarize, "priority" : sum_pririty})

        higest_priority_list = sorted(result, key=lambda d: d['priority'], reverse=True)[0]["result"]
        return higest_priority_list
    
    def is_coin(self, bill):
        return FUND_TYPES[bill] == 'COIN'


    def update_funds(self, update_bills, action = 'withdrawl'):
        sign = -1
        if action == 'refill':
            sign = 1
        
        for bill, amount in update_bills.items():
            self.funds[float(bill)] = self.funds.setdefault(float(bill), 0) + sign *amount

        return True
    
    def validate_withdrawl(self, amount):
        if amount > MAX_WITHDRAWAL_AMOUNT:
            raise UnprocessableEntity
        else:
            return True
    
    def validate_funds(self, funds):
        if len(list(filter(lambda bill: float(bill) not in FUND_TYPES.keys() ,funds.keys()))) > 0:
            raise UnprocessableEntity
        else:
            return True
        

atm = ATMMachine(initial_funds = {200: 1, 100: 2, 20: 5, 10: 0, 5: 0, 1: 2, 0.1: 1, 0.01: 10})

