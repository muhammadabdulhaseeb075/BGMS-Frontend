from django.core.cache import caches
import pickle

class Cache(object):

    cache = caches['default']

    def set_cache(self, cache_alias):
        self.cache = caches[cache_alias]

    def cache_queryset(self, key, queryset):
        pickle_string = pickle.dumps(queryset)
        self.cache.set(key, pickle_string)

    def get_queryset(self, key):
        expired = None
        pickle_string = self.cache.get(key, expired)
        if pickle_string is not expired:
            return pickle.loads(pickle_string)
        else:
            return expired

    def delete_key(self, key):
        self.cache.delete(key)