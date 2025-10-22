"""
Configuración del Sistema de Análisis de Ventas
"""

class AppConfig:
    # Configuración de la aplicación
    APP_NAME = "Sales Analysis Pro"
    VERSION = "2.0.0"
    AUTHOR = "Anabel Moreno"
    
    # Configuración de datos
    DEFAULT_RECORDS = 2000
    DATA_RETENTION_DAYS = 365
    
    # Configuración de análisis
    TREND_ANALYSIS_DAYS = 90
    PREDICTION_CONFIDENCE_THRESHOLD = 0.7
    
    # Configuración de UI
    THEME = "default"
    CHART_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    # Configuración de reportes
    ENABLE_LOGGING = True
    LOG_LEVEL = "INFO"
    
    @classmethod
    def get_config_summary(cls):
        """Resumen de configuración para logging"""
        return {
            'app_name': cls.APP_NAME,
            'version': cls.VERSION,
            'default_records': cls.DEFAULT_RECORDS,
            'theme': cls.THEME
        }