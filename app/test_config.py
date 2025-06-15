from app.core.config import Settings

def test_settings():
    settings = Settings()
    print(f"Project Name: {settings.PROJECT_NAME}")
    print("Settings loaded successfully!")

if __name__ == "__main__":
    test_settings() 