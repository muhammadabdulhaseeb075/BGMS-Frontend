
from tenant_schemas.postgresql_backend.introspection import DatabaseSchemaIntrospection as TenantIntrospection
from django.contrib.gis.db.backends.postgis.introspection import PostGISIntrospection

class Introspection(PostGISIntrospection,TenantIntrospection):
	pass
