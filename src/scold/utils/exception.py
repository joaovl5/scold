class ScoldException(Exception):
    def __init__(
        self,
        message: str | None = None,
        *args: object,
        **kwargs: object,
    ) -> None:
        self.message: str | None = message
        super().__init__(*args, **kwargs)
