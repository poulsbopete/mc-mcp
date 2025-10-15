"""Configuration management for Mastercard Demo with OpenTelemetry."""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Mastercard API Configuration
    mastercard_api_key: str = Field(default="", env="MASTERCARD_API_KEY")
    mastercard_consumer_key: str = Field(default="", env="MASTERCARD_CONSUMER_KEY")
    mastercard_private_key_path: str = Field(default="", env="MASTERCARD_PRIVATE_KEY_PATH")
    mastercard_keystore_password: str = Field(default="", env="MASTERCARD_KEYSTORE_PASSWORD")
    
    # Elastic Configuration
    elastic_otlp_endpoint: str = Field(
        default="https://a5630c65c43f4f299288c392af0c2f45.ingest.us-east-1.aws.elastic.cloud:443",
        env="ELASTIC_OTLP_ENDPOINT"
    )
    elastic_otel_api_key: str = Field(
        default="UHNLemtaa0JrZlJTcENQM1UwczE6aDdjaEJUMjlXd1lKNGFhMEpJZzV2UQ==",
        env="ELASTIC_OTEL_API_KEY"
    )
    elasticsearch_url: str = Field(
        default="https://a5630c65c43f4f299288c392af0c2f45.es.us-east-1.aws.elastic.cloud",
        env="ELASTICSEARCH_URL"
    )
    elasticsearch_api_key: str = Field(
        default="Z0pQRmtaa0IxRllTajhaRjUtNUk6ZEtNbDQyTTFMdGVzS1diOXpnWEZSUQ==",
        env="ELASTICSEARCH_API_KEY"
    )
    
    # Application Configuration
    service_name: str = Field(default="mastercard-demo", env="SERVICE_NAME")
    service_version: str = Field(default="1.0.0", env="SERVICE_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Demo Configuration
    enable_mock_mode: bool = Field(default=True, env="ENABLE_MOCK_MODE")
    demo_port: int = Field(default=8000, env="DEMO_PORT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

