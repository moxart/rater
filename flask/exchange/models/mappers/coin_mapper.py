def mapFromEntity(entity):
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


def mapFromEntityList(entityList):
    return list(map(mapFromEntity, entityList))
