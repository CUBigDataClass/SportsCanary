def american_to_decimal(num):
    num = float(num)
    if num > 0:
        num = (num / 100) + 1
    elif num < 0:
        num = (100 / abs(num)) + 1
    return float("%.3f" % num)


def decimal_to_american(num):
    num = abs(float(num))
    if num >= 2.00:
        return (num - 1) * 100
    elif num < 2.00:
        return (-100) / (num - 1)
