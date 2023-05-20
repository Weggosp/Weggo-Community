from ._ext import env

class Filters:
    
    ## SORT FOR ARRAYS IN TEMPLATES
    def deep_sort(value, attribute, subattribute):
        return sorted(value, key=lambda element: element[attribute][0][subattribute])

    env.filters['deep_sort'] = deep_sort