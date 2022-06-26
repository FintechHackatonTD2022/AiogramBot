

class Validator:
    @classmethod
    def validate_amount(cls, amount: int) -> bool:
        try:
            int(amount)
            return True
        except:
            return False

    @classmethod
    def validate_iin(cls, iin: int) -> bool:
        if len(iin) == 12:
            return True
        return False
