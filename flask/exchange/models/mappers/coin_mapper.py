from exchange.models.coin_commercial import CoinCommercial
from exchange.models.coin_single import CoinSingle
from slugify import slugify


def map_from_entity(entity):
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


def map_to_single_entity(coin):
    return CoinSingle(
        title=coin['title'],
        slug=slugify(coin['title']),
        price=coin['prices'][0]['live'],
        change=coin['prices'][0]['change'],
        min=coin['prices'][0]['min'],
        max=coin['prices'][0]['max'],
        updated_at=coin['time']
    )


def map_to_commercial_entity(coin):
    return CoinCommercial(
        title=coin['title'],
        slug=slugify(coin['title']),
        price=coin['prices'][0]['live'],
        change=coin['prices'][0]['change'],
        min=coin['prices'][0]['min'],
        max=coin['prices'][0]['max'],
        updated_at=coin['time']
    )


def map_from_entity_list(entity_list):
    return list(map(map_from_entity, entity_list))
