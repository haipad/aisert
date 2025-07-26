import logging


class AIsertConfig:
    """
    Configuration class for AIsert.
    This class holds the configuration settings for the AIsert application.
    """

    _MODE = ["lite", "full"]

    logger = logging.getLogger("AIsertConfig")

    def __init__(
        self,
        token_encoding: str,
        token_model: str,
        api_key: str = None,
        mode: str = "lite",
        sentence_transformer_model: str = "all-MiniLM-L6-v2",
    ):
        self.logger = logging.getLogger(self.__class__.__name__)

        if mode not in self._MODE:
            mode = self._MODE[0]
            self.logger.error(
                f"Invalid mode: {mode}. Next time choose from {self._MODE}. Defaulting to 'lite'."
            )
        self.mode = mode
        self.token_encoding = token_encoding
        self.token_model = token_model
        if self.mode == "lite":
            sentence_transformer_model = None
        self.sentence_transformer_model = sentence_transformer_model

    @staticmethod
    def get_default_config():
        """
        Returns the default configuration for AIsert.
        """
        return AIsertConfig(
            mode="lite",
            token_encoding=None,
            token_model="openai",
            sentence_transformer_model="all-MiniLM-L6-v2",
        )

    @staticmethod
    def load_from_json(file_path):
        """
        Loads the configuration from a JSON file.
        :param file_path: Path to the JSON configuration file.
        :return: An instance of AIsertConfig with the loaded settings.
        """
        import json

        try:
            with open(file_path, "r") as f:
                try:
                    config_data = json.load(f)
                except json.JSONDecodeError as e:
                    AIsertConfig.logger.error(
                        f"Error decoding JSON from {file_path}: {e}"
                    )
                    return AIsertConfig.get_default_config()
        except FileNotFoundError:
            AIsertConfig.logger.error(f"Configuration file {file_path} not found.")
            return AIsertConfig.get_default_config()
        return AIsertConfig(**config_data)


    def __repr__(self):
        return (
            f"AIsertConfig(mode={self.mode}, "
            f"token_encoding={self.token_encoding}, "
            f"token_model={self.token_model}, "
            f"sentence_transformer_model={self.sentence_transformer_model})"
        )
