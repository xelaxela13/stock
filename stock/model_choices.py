ORDER_IN, ORDER_OUT = range(2)
ORDER_TYPE = (
    (ORDER_IN, 'Приходная накладная'),
    (ORDER_OUT, 'Расходная накладная')
)
DISCOUNT_AMOUNT = 'amount'
DISCOUNT_PERCENT = 'percent'
DISCOUNT_TYPE = (
    (DISCOUNT_AMOUNT, 'Грн.'),
    (DISCOUNT_PERCENT, '%'),
)
