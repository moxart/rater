from exchange.models.currency import Currency


def mapFromEntity(entity):
    return {
        "title": entity['title'],
        "codes": [{
            "alpha2": entity['alpha2'],
            "alpha3": entity['alpha3']
        }],
        "country": entity['country'],
        "prices": [{
            "live": entity['price'],
            "change": entity['change'],
            "min": entity['min'],
            "max": entity['max']
        }],
        "time": entity['updated_at']
    }


def mapToEntity(currency):
    return Currency(
        title=currency['title'],
        alpha2=currency['codes'][0]['alpha2'],
        alpha3=currency['codes'][0]['alpha3'],
        country=currency['country'],
        price=currency['prices'][0]['live'],
        change=currency['prices'][0]['change'],
        min=currency['prices'][0]['min'],
        max=currency['prices'][0]['max'],
        updated_at=currency['time']
    )


def mapFromEntityList(entityList):
    return list(map(mapFromEntity, entityList))
