import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
from datetime import datetime
from config import AppConfig
from data_generator import generate_sales_data
from analysis_engine import SalesAnalyzer
from visualization import SalesVisualizer
class SalesAnalysisPro:
    def __init__(self, root):
        self.root = root
        self.config = AppConfig()
        self.setup_app()
        self.initialize_data()
        self.create_main_interface()
        
        # Log de inicio
        self.logger.info(f"Aplicación {self.config.APP_NAME} v{self.config.VERSION} iniciada")
    
    def setup_app(self):
        """Configuración inicial de la aplicación"""
        self.root.title(f"{self.config.APP_NAME} v{self.config.VERSION}")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configurar logging
        if self.config.ENABLE_LOGGING:
            logging.basicConfig(
                level=getattr(logging, self.config.LOG_LEVEL),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('app.log'),
                    logging.StreamHandler()
                ]
            )
        self.logger = logging.getLogger(__name__)
    
    def initialize_data(self):
        """Inicialización y verificación de datos"""
        try:
            self.analyzer = SalesAnalyzer()
            self.logger.info("Datos cargados exitosamente")
        except FileNotFoundError:
            self.logger.info("Generando datos iniciales...")
            response = messagebox.askyesno(
                "Datos No Encontrados", 
                "No se encontraron datos de ventas. ¿Generar datos de demostración?"
            )
            if response:
                generate_sales_data(self.config.DEFAULT_RECORDS)
                self.analyzer = SalesAnalyzer()
                messagebox.showinfo("Éxito", 
                                  f"Se generaron {self.config.DEFAULT_RECORDS} registros de demostración")
            else:
                self.root.destroy()
                return
        
        self.visualizer = SalesVisualizer(self.analyzer)
    
    def create_main_interface(self):
        """Interfaz principal mejorada"""
        # Barra de menú
        self.create_menu_bar()
        
        # Panel principal
        main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel lateral (sidebar)
        self.sidebar = self.create_sidebar(main_panel)
        main_panel.add(self.sidebar)
        
        # Panel de contenido principal
        self.content_frame = ttk.Frame(main_panel)
        main_panel.add(self.content_frame)
        
        # Mostrar dashboard por defecto
        self.show_dashboard()
    
    def create_menu_bar(self):
        """Barra de menú profesional"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Regenerar Datos", command=self.regenerate_data)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Análisis
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Análisis", menu=analysis_menu)
        analysis_menu.add_command(label="Dashboard", command=self.show_dashboard)
        analysis_menu.add_command(label="Ventas por Categoría", command=self.show_category_analysis)
        analysis_menu.add_command(label="Análisis de Productos", command=self.show_product_analysis)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)
    
    def create_sidebar(self, parent):
        """Panel lateral con métricas rápidas"""
        sidebar = ttk.Frame(parent, width=250)
        
        # Header del sidebar
        header = ttk.Label(sidebar, text="Métricas Rápidas", 
                          style='Title.TLabel')
        header.pack(pady=10)
        
        # Métricas en tiempo real
        self.update_sidebar_metrics(sidebar)
        
        # Botones de acción rápida
        actions_frame = ttk.Frame(sidebar)
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(actions_frame, text="📊 Dashboard", 
                  command=self.show_dashboard).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="🔄 Actualizar", 
                  command=self.refresh_data).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="📈 Tendencias", 
                  command=self.show_trend_analysis).pack(fill=tk.X, pady=2)
        
        return sidebar
    
    def update_sidebar_metrics(self, sidebar):
        """Actualizar métricas en el sidebar"""
        # Limpiar métricas anteriores
        for widget in sidebar.winfo_children():
            if isinstance(widget, ttk.Frame) and widget != sidebar.winfo_children()[0]:
                widget.destroy()
        
        stats = self.analyzer.get_summary_stats()
        trend = self.analyzer.sales_trend_analysis()
        
        unique_customers = len(set([f"{r['region']}_{r['customer_type']}" for r in self.analyzer.data]))
        
        metrics = [
            ("Ventas Hoy", f"${stats.get('sales_today', 0):,.0f}"),
            ("Crecimiento", f"{trend['average_weekly_growth']}%"),
            ("Órdenes", f"{stats['total_orders']}"),
            ("Clientes", f"{unique_customers}")
        
        ]
        
        for title, value in metrics:
            metric_frame = ttk.Frame(sidebar)
            metric_frame.pack(fill=tk.X, padx=10, pady=3)
            
            ttk.Label(metric_frame, text=title, width=12).pack(side=tk.LEFT)
            ttk.Label(metric_frame, text=value, style='Value.TLabel').pack(side=tk.RIGHT)
    
    def clear_content(self):
        """Limpiar el área de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Mostrar dashboard principal"""
        self.clear_content()
        self.visualizer.create_dashboard(self.content_frame)
        self.logger.info("Dashboard mostrado")
    
    def show_category_analysis(self):
        """Mostrar análisis por categoría"""
        self.clear_content()
        self.visualizer.create_category_chart(self.content_frame)
        self.logger.info("Análisis por categoría mostrado")
    
    def show_product_analysis(self):
        """Mostrar análisis de productos"""
        self.clear_content()
        self.visualizer.create_product_analysis(self.content_frame)
    
    def show_trend_analysis(self):
        """Mostrar análisis de tendencias"""
        self.clear_content()
        self.visualizer.create_trend_analysis(self.content_frame)
    
    def refresh_data(self):
        """Refrescar datos y vistas"""
        self.analyzer = SalesAnalyzer()
        self.visualizer = SalesVisualizer(self.analyzer)
        self.update_sidebar_metrics(self.sidebar)
        self.show_dashboard()
        messagebox.showinfo("Éxito", "Datos actualizados correctamente")
        self.logger.info("Datos refrescados")
    
    def regenerate_data(self):
        """Regenerar datos de demostración"""
        if messagebox.askyesno("Confirmar", "¿Regenerar todos los datos? Los datos existentes se perderán."):
            generate_sales_data(self.config.DEFAULT_RECORDS)
            self.refresh_data()
            self.logger.info("Datos regenerados")
    
    def show_about(self):
        """Mostrar información acerca de la aplicación"""
        about_text = f"""
{self.config.APP_NAME} v{self.config.VERSION}

Sistema de análisis de ventas 100% offline
Desarrollado por {self.config.AUTHOR}

Características:
• Análisis de ventas en tiempo real
• Tendencias y predicciones
• Dashboard interactivo
• 100% offline - Zero dependencias

© 2024 - Todos los derechos reservados
"""
        messagebox.showinfo("Acerca de", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesAnalysisPro(root)
    root.mainloop()