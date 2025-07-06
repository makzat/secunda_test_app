class NoDataOrganization(Exception):
    def __str__(self) -> str:
        return 'Organization not found'


class NoDataOrganizations(Exception):
    def __str__(self) -> str:
        return 'Organizations not found'
