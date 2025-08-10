import logging

from aisert.config.defaults import DefaultConfig


class AIsertConfig:
    """
    Configuration class for AIsert.
    This class holds the configuration settings for the AIsert application.
    """
    logger = logging.getLogger("AIsertConfig")

    def __init__(
        self,
        model_provider,
        token_model: str,
        token_encoding: str = None,
        sentence_transformer_model: str = "all-MiniLM-L6-v1",
    ):
        """
        Initializes the AIsertConfig with the provided parameters.
        :param token_encoding: The encoding type for tokens (applicable only for openAI models).
        :param token_model: The model used for tokenization.
        :param model_provider: The provider of the LLM model being used.
        :param sentence_transformer_model: The sentence transformer model used for semantic validation.
        """
        self.mode = "default"
        self.logger = logging.getLogger(self.__class__.__name__)

        self.token_encoding = token_encoding
        self.token_model = token_model
        self.model_provider = model_provider
        self.sentence_transformer_model = sentence_transformer_model

    @staticmethod
    def get_default_config():
        """
        Returns the default configuration for AIsert.
        """
        default_config = DefaultConfig.to_dict()
        return AIsertConfig(**default_config)

    @staticmethod
    def load(file_path: str) -> "AIsertConfig":
        """
        Loads the configuration from a JSON file.
        :param file_path: Path to the JSON configuration file.
        :return: An instance of AIsertConfig with the loaded settings.
        """
        import json
        import os

        #Sanitize file path
        file_path = os.path.abspath(file_path)
        try:
            with open(file_path, "r") as f:
                try:
                    config_data = json.load(f)
                except json.JSONDecodeError as e:
                    AIsertConfig.logger.error(
                        f"Error decoding JSON from {file_path}: {e}"
                    )
                    AIsertConfig.logger.info("Using default configuration.")
                    return AIsertConfig.get_default_config()
        except FileNotFoundError:
            AIsertConfig.logger.error(f"Configuration file {file_path} not found.")
            AIsertConfig.logger.info(f"Using default configuration.")
            return AIsertConfig.get_default_config()
        return AIsertConfig(**config_data)


    def __repr__(self):
        return (
            f"AIsertConfig(token_encoding={self.token_encoding}, "
            f"token_model={self.token_model}, "
            f"model_provider={self.model_provider}, "
            f"sentence_transformer_model={self.sentence_transformer_model})"
        )
