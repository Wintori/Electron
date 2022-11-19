from pydantic import BaseSettings


class Settings(BaseSettings):
    db_name: str = "postres"
    db_user: str = "postres"
    db_password: str = "postres"
    db_host: str = "pg:5432"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_url: str = "127.0.0.1"
    db_port: int = 5432
    # db_name: str = "test_task"
    server_host: str = "127.0.0.1"
    server_port: int = 8080

    @property
    def db_settings(self):
        return self

    def get_dsn_sync(self):
        return f'postgresql+psycopg2://{self.db_name}:{self.db_password}' \
               f'@{self.db_url}:{self.db_port}/{self.db_name}'
