# -*- coding: utf-8 -*-
'''
currency exchange

input and expected ouput:
2 8 2 127 HKD MAX => GBP 3 USD 1 CYN 7 HKD 1
2 8 2 127 HKD max => ERROR
2 8 2 20 CNY MIN => 20 HKD
'''


def is_int(args):
    '''
    判断为整数，不是小数
    '''
    for i in range(4):
        if not args[i].isdigit():
            return False
    return True


def check_args(cny_to_hkd, usd_to_cny, gbp_to_usd, val):
    if cny_to_hkd > 0 and usd_to_cny > 0 and gbp_to_usd > 0 and val > 0:
        if isinstance(cny_to_hkd, int) and isinstance(usd_to_cny, int) and isinstance(gbp_to_usd, int) and isinstance(val, int):
            return True
    return False


def currency(cny_to_hkd, usd_to_cny, gbp_to_usd, value, val_type, ch_type):
    val = 0
    if val_type == 'CYN':
        val = value * cny_to_hkd
    elif val_type == 'USD':
        val = value * usd_to_cny * cny_to_hkd
    elif val_type == 'GBP':
        val = value * gbp_to_usd * usd_to_cny * cny_to_hkd
    else:
        val = value

    # MIN
    if ch_type == 'MIN':
        return 'HKD %d' % val

    # MAX
    tmp = gbp_to_usd * usd_to_cny * cny_to_hkd
    gbp = val / tmp
    remained = val % tmp
    if remained == 0:
        return 'GBP %d' % gbp

    tmp = usd_to_cny * cny_to_hkd
    usd = remained / tmp
    remained = remained % tmp
    if remained == 0:
        return 'GBP %d USD %d' % (gbp, usd)

    tmp = cny_to_hkd
    cyn = remained / tmp
    remained = remained % tmp
    if remained == 0:
        return 'GBP %d USD %d CYN %d' % (gbp, usd, cyn)
    else:
        return 'GBP %d USD %d CYN %d HKD %d' % (gbp, usd, cyn, remained)


if __name__ == '__main__':
    import sys
    for input in sys.stdin:
        input = input.strip('\r\n')
        if input.lower() == 'exit':
            print('bye')
            exit(0)

        args = input.split(' ')
        if len(args) < 6:
            print('ERROR')
            continue

        if not is_int(args):
            print('ERROR')
            continue

        try:
            cny_to_hkd = int(args[0])
            usd_to_cny = int(args[1])
            gbp_to_usd = int(args[2])
            val = int(args[3])
        except ValueError as e:
            print('ERROR')
            continue
        val_type = args[4]
        ch_type = args[5]

        if not check_args(cny_to_hkd, usd_to_cny, gbp_to_usd, val):
            print('ERROR')
            continue

        if val_type not in ('HKD', 'CNY', 'USD', 'GBP'):
            print('ERROR')
            continue

        if ch_type not in ('MIN', 'MAX'):
            print('ERROR')
            continue

        print(currency(cny_to_hkd, usd_to_cny, gbp_to_usd, val, val_type, ch_type))
