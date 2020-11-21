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

def mapFromEntityList(entityList):
    return list(map(mapFromEntity, entityList))