from storages.backends.s3boto import S3BotoStorage

from django.conf import settings

class TenantMediaStorage(S3BotoStorage):
	# overwriting S3BotoStorage attributes with tenant specific value
	file_overwrite = False
	bucket_name = settings.AWS_MEDIA_BUCKET_NAME
	custom_domain = None
	default_acl = 'authenticated-read'
	# def path(self, name):
	# 	return self._normalize_name(name)

	# overwriting the bucket property to use a tenant specific bucket
# 	@property
# 	def bucket(self):
# 		"""
# 		Get the current bucket. If there is no current bucket object
# 		create it.
# 		"""
# 		key = connection.schema_name
# 		bucket_tuple = self.bucket_dict.get(key)
# 		if(bucket_tuple is None):
# 			bucket_name = BurialGroundSite.objects.get(schema_name=key).aws_media_bucket
# 			# using super class private method here - need to find a better way
# 			bucket = super(TenantMediaStorage, self)._get_or_create_bucket(bucket_name)
# 			print(bucket_name)
# 			bucket_tuple = self.bucket_dict[key] = (bucket_name, bucket)
# 			print('bucket'+bucket_name+'added to dict')
# 		else:
# 			print('bucket for'+key+'fetched from dict')
# 		# overwriting S3BotoStorage attributes with tenant specific value
# 		self.bucket_name = None
# 		self.custom_domain = None
# 		return bucket_tuple[1]
