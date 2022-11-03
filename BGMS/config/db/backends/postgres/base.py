from tenant_schemas.postgresql_backend.base import DatabaseWrapper as TenantWrapper
from django.contrib.gis.db.backends.postgis.base import DatabaseWrapper as GeodjangoDatabaseWrapper
from config.db.backends.postgres.introspection import Introspection


class DatabaseWrapper(GeodjangoDatabaseWrapper,TenantWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.introspection = Introspection(self)