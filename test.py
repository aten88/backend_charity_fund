
LIST_DATA = [1000, 1000, 1000]


data = {
    'full_amount': 1500,
    'invested_amount': 0,
    'fully_invested': False
}


def invest(donations):
    ostatok = 500
    for donat in donations:

        if data['fully_invested']:
            break

        if ostatok:
            data['invested_amount'] += ostatok

        if donat == data['full_amount']:
            data['invested_amount'] = donat
            difference = data['full_amount'] - data['invested_amount']
            data['fully_invested'] = True
            ostatok += difference

        if donat > data['full_amount']:
            difference = donat - data['full_amount']
            data['invested_amount'] = donat - difference
            data['full_amount'] = donat - difference
            data['fully_invested'] = True
            ostatok += difference

        if donat < data['full_amount']:
            difference = data['full_amount'] - donat
            data['invested_amount'] = data['full_amount'] - difference

    print(ostatok)

    return data


print(invest(LIST_DATA))
