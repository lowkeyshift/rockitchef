from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

# this page will be used to import defaults when creating templates
# in the future.
class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10
