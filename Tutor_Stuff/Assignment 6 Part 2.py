

def main():
    count = int(input("Enter the number of inputs: "))
    for var1 in range(count):
        result = get_input(var1)
        print_output(result, var1)
       



def get_input(count):
    EVEN_EXP = False
    NEG_EXP = False
    NEG_BASE = False

    base = int(input("\nEnter base {}    : ".format(count+1)))
    exp = int(input("Enter exponent {}   : ".format(count+1)))



    if exp%2 == 0:
        EVEN_EXP = True
    if exp < 0:
        NEG_EXP = True
    if base < 0:
        NEG_BASE = True

    print 'Even Exp: {}'.format(EVEN_EXP)
    print 'NEG_EXP: {}'.format(NEG_EXP)
    print 'NEG_BASE: {}'.format(NEG_BASE)

    return expon(base, exp, NEG_EXP, EVEN_EXP, NEG_BASE)
    



def expon(base, exp, NEG_EXP, EVEN_EXP, NEG_BASE):
    if not exp or base == 1:
        return 1
    if not base or exp == 1:
        print 'Here'
        return base
    if exp == 2 and not NEG_BASE:
        return mult(base, base)

    base = abs(base)
    exp = abs(exp)

    

    if exp == 1 and NEG_EXP:
        return 1/float(base)
    if (exp == 2 and NEG_EXP) or (exp == 2 and NEG_BASE):
        return 1/float(mult(base, base))

    for count in range(exp-2):
        print 'base: {}'.format(base)

        if count == 0:
            print '1st Run'
            new_base = mult(base, base)

        print 'running'
        new_base = mult(new_base, base)
        print 'new_base: {}'.format(new_base)

    ## Check Flags
    if NEG_BASE and not EVEN_EXP:
        print 'ODD EXP and NEGATIVE BASE'
        print 'result: {}'.format(-new_base)
        return -new_base

    print 'NEG_EXP {}'.format(NEG_EXP)
    if NEG_EXP:
        print 'NEG_EXP'
        return 1/float(new_base)

    return new_base


def mult(base, count):

    product = base

    for var1 in range(count-1):
        product += base

    return product


        


def print_output(result, count):
    print("result  {}    : ".format(count+1) + str(result))


if __name__ == '__main__':
    main()
    #a = get_input(1)
    #print 'result: {}'.format(a)


#main()


