# '''
# Created on 25 Nov 2015

# @author: achickermane
# '''
# from compressor.filters import CompilerFilter
# from django.conf import settings

# class UglifyFilter(CompilerFilter):
#     command = "{binary} {args}"
#     options = (
#         ("binary", 'uglifyjs'),
#         ("args", settings.COMPRESS_UGLIFYJS_ARGUMENTS),
#     )