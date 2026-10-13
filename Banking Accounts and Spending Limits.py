class Account:
    def __init__(self, account_id, holder, currency, opening_balance, account_type="Basic", daily_limit=0):
        self._account_id = account_id
        self.holder = holder
        self.currency = currency
        self._balance = int(opening_balance)
        self.account_type = account_type
        self._daily_limit = int(daily_limit)
        self._ledger = []

    def _check_debit(self, amount):
        amount = int(amount)
        if amount > self._balance:
            raise ValueError("Balance is too low for this debit")
        return True

    def credit(self, amount):
        amount = int(amount)
        self._balance += amount
        self._ledger.append({
            "kind": "credit",
            "amount": amount,
            "account_id": self._account_id
        })
        return True

    def debit(self, amount):
        amount = int(amount)
        if self.account_type == "Travel" and amount > self._daily_limit:
            raise ValueError(f"Travel debit exceeds the limit of {self._daily_limit} units")
        
        self._check_debit(amount)
        self._balance -= amount
        self._ledger.append({
            "kind": "debit",
            "amount": amount,
            "account_id": self._account_id
        })
        return True

    def get_balance(self):
        return self._balance

    def get_ledger(self, kind=None):
        valid_kinds = ["credit", "debit"]
        if kind is not None and kind not in valid_kinds:
            raise ValueError("Unknown transaction kind")
            
        records = self._ledger
        if kind is not None:
            records = [r for r in records if r["kind"] == kind]
        return [dict(r) for r in records]

    def get_daily_limit(self):
        return self._daily_limit
