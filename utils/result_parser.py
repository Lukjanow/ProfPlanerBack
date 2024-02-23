def remove_mongo_id(result):
    result.pop("_id")
    return result


def remove_mongo_ids(results):
    x = []
    for result in results:
        result.pop("_id")
        x.append(result)
    return x