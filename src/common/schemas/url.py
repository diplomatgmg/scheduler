from typing import ClassVar

from pydantic.networks import AnyUrl


class HttpsUrl(AnyUrl):
    allowed_schemes: ClassVar = ["https"]
