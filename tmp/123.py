def delta(number: list):
    return abs(sum(number[:3]) - sum(number[3:]))

def getUpperLuckyTicket1(number):
    ''' Nearest ticket upper if s1 > s2 '''
    for i in range(len(number) - 1, 0, -1):
        if number[i] + delta(number) <= 9:
            number[i] += delta(number)
            return "".join([str(n) for n in number])
        number[i] = 9

def getLowerLuckyTicket1(number):
    ''' Nearest ticket lower if s1 < s2 '''
    for i in range(len(number) - 1, 0, -1):
        if number[i] - delta(number) >= 0:
            number[i] -= delta(number)
            return "".join([str(n) for n in number])
        number[i] = 0

def getUpperLuckyTicket2(number):
    ''' Nearest ticket upper if s1 < s2 '''
    for i in range(len(number) - 2, -1, -1):
        if number[i] != 9:
            number[i] += 1
            for j in range(i + 1, len(number)):
                number[j] = 0
            if sum(number[:3]) >= sum(number[3:]):
                return getUpperLuckyTicket1(number)
    return "0"


def getLowerLuckyTicket2(number):
    ''' Nearest ticket upper if s1 > s2 '''
    for i in range(len(number) - 2, -1, -1):
        if number[i] != 0:
            number[i] -= 1
            for j in range(i + 1, len(number)):
                number[j] = 9
            if sum(number[:3]) <= sum(number[3:]):
                return getLowerLuckyTicket1(number)
    return "0"


def isLucky(ticket):
    return sum([int(n) for n in str(ticket)[:3]]) == \
            sum([int(n) for n in str(ticket)[3:]])

def test():
    with open("log.txt", "w") as f:
        for i in range(200_000, 700_000 + 1):
            ticket = i
            while not isLucky(ticket):
                ticket += 1
            
            number = [int(n) for n in str(i)]
            try:
                if sum([int(n) for n in str(i)[:3]]) < sum([int(n) for n in str(i)[3:]]) and \
                   ticket != int(getUpperLuckyTicket2(number)):
                    f.writelines(f"{i} -> {ticket} | {int(getUpperLuckyTicket2(number))}\n")
            except ValueError as e:
                f.writelines(f"{i} -> {ticket}\n")

test()
# print(getLowerLuckyTicket2([int(n) for n in "207010"]))
print("Done")

