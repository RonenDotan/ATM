from collections import Counter
from DB import db
from env_variables import CONSTANTS, FUND_TYPES, ATM_ID

class UnprocessableEntity(Exception):
    message = "UnprocessableEntity"
    status_code = 422

class conflict(Exception):
    message = "conflict"
    status_code = 409


class ATMMachine:
    def __init__(self, atm_id):
        self.atm_id = atm_id
        self.funds = db.get_funds(self.atm_id)

    def calculate_withdrawl(self, amount):
        withdrawl_options = []
        solution_without_coins_limit = False

        def internal_withdrawl_calculation(amount, atm_content, output, total_coins):
            nonlocal solution_without_coins_limit
            if len(withdrawl_options) >= 3:
                return
            for curr_bill, bill_amount in atm_content.items():
                if bill_amount == 0:
                    continue

                if self.is_coin(curr_bill):
                    total_coins += 1
                    if total_coins > CONSTANTS['MAX_COINS']:
                        if solution_without_coins_limit:
                            return

                if curr_bill == amount:
                    if total_coins > CONSTANTS['MAX_COINS']:
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
    
    def prioritize_withdrawl_option(self, withdrawl_options, solution_without_coins_limit ,priority_weight = {200: 200*200, 100: 100*100, 50: 50*50, 20: 20*20, 10: 10*10, 5:5*5, 1: 1, 0.1: 0.1, 0.01:0.01}):
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

        db.update_funds(self.atm_id, self.funds)
        return True
    
    def validate_withdrawl(self, amount):
        if amount > CONSTANTS['MAX_WITHDRAWAL_AMOUNT']:
            raise UnprocessableEntity
        else:
            return True
    
    def validate_funds(self, funds):
        if len(list(filter(lambda bill: float(bill) not in FUND_TYPES.keys() ,funds.keys()))) > 0:
            raise UnprocessableEntity
        else:
            return True
        
    def clean_result(self, withdrawl_bils):
        def try_round_bill(bill):
            if bill == int(bill):
                return int(bill)
            else:
                return bill

        result = {}
        for bill, amount in withdrawl_bils.items():
            round_bill = try_round_bill(bill)
            result.setdefault(FUND_TYPES[bill],{})
            result[FUND_TYPES[bill]].setdefault(round_bill, amount)
        return {"result": result}


atm = ATMMachine(atm_id = ATM_ID)


