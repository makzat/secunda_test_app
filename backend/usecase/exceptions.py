class NoDataOrganization(Exception):
    def __str__(self) -> str:
        return f"Organization not found"


class NoDataOrganizations(Exception):
    def __str__(self) -> str:
        return f"Organizations not found"
