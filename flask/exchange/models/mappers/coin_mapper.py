from exchange.models.coin_commercial import CoinCommercial
from exchange.models.coin_single import CoinSingle
from slugify import slugify


def mapFromEntity(entity):
    print(entity)
    return {
        "title": entity['title'],
        "prices": [{
            "live": entity['price'],
            "change": entity['change'],
            "min": entity['min'],
            "max": entity['max']
        }],
        "time": entity['updated_at']
    }


def mapToSingleEntity(coin):
    return CoinSingle(
        title=coin['title'],
        slug=slugify(coin['title']),
        price=coin['prices'][0]['live'],
        change=coin['prices'][0]['change'],
        min=coin['prices'][0]['min'],
        max=coin['prices'][0]['max'],
        updated_at=coin['time']
    )


def mapToCommercialEntity(coin):
    return CoinCommercial(
        title=coin['title'],
        slug=slugify(coin['title']),
        price=coin['prices'][0]['live'],
        change=coin['prices'][0]['change'],
        min=coin['prices'][0]['min'],
        max=coin['prices'][0]['max'],
        updated_at=coin['time']
    )


def mapFromEntityList(entityList):
    return list(map(mapFromEntity, entityList))
