import tkinter as tk
from tkinter import ttk
from datetime import datetime

class SalesVisualizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.setup_styles()
    
    def setup_styles(self):
        """Configuración de estilos profesionales"""
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Metric.TLabel', font=('Arial', 11, 'bold'))
        self.style.configure('Value.TLabel', font=('Consolas', 10))
        self.style.configure('Success.TLabel', foreground='green')
        self.style.configure('Warning.TLabel', foreground='orange')
    
    def create_dashboard(self, parent):
        """Dashboard completo con múltiples métricas"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título principal
        title = ttk.Label(frame, text="📊 Dashboard de Ventas - Análisis Completo", 
                         style='Title.TLabel')
        title.pack(pady=(0, 20))
        
        # Métricas principales en grid
        metrics_frame = ttk.Frame(frame)
        metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.create_metrics_grid(metrics_frame)
        
        # Gráficos
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de tendencias
        trend_frame = ttk.Frame(notebook)
        notebook.add(trend_frame, text="📈 Tendencias")
        self.create_trend_analysis(trend_frame)
        
        # Pestaña de productos
        product_frame = ttk.Frame(notebook)
        notebook.add(product_frame, text="🏆 Productos")
        self.create_product_analysis(product_frame)
        
        # Pestaña de clientes
        customer_frame = ttk.Frame(notebook)
        notebook.add(customer_frame, text="👥 Clientes")
        self.create_customer_analysis(customer_frame)
        
        return frame
    
    def create_metrics_grid(self, parent):
        """Grid de métricas clave"""
        stats = self.analyzer.get_summary_stats()
        trend_analysis = self.analyzer.sales_trend_analysis()
        customer_analysis = self.analyzer.customer_analysis()
        
        # Fila 1
        row1 = ttk.Frame(parent)
        row1.pack(fill=tk.X, pady=5)
        
        self.create_metric_card(row1, "Ventas Totales", 
                               f"${stats['total_sales']:,.2f}", 0)
        self.create_metric_card(row1, "Crecimiento Semanal", 
                               f"{trend_analysis['average_weekly_growth']}%", 1)
        self.create_metric_card(row1, "Valor Promedio Orden", 
                               f"${customer_analysis['average_order_value']:,.2f}", 2)
        
        # Fila 2
        row2 = ttk.Frame(parent)
        row2.pack(fill=tk.X, pady=5)
        
        self.create_metric_card(row2, "Total Órdenes", 
                               f"{stats['total_orders']:,}", 0)
        self.create_metric_card(row2, "Semanas Analizadas", 
                               f"{trend_analysis['total_weeks']}", 1)
        self.create_metric_card(row2, "Segmentos Cliente", 
                               f"{customer_analysis['customer_segments']}", 2)
    
    def create_metric_card(self, parent, title, value, column):
        """Tarjeta de métrica individual"""
        card = ttk.Frame(parent, relief='solid', borderwidth=1)
        card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(card, text=title, style='Metric.TLabel').pack(pady=(8, 2))
        ttk.Label(card, text=value, style='Value.TLabel').pack(pady=(2, 8))
    
    def create_trend_analysis(self, parent):
        """Análisis de tendencias temporal"""
        trend_data = self.analyzer.sales_trend_analysis()
        predictive = self.analyzer.predictive_insights()
        
        # Frame con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tendencias semanales
        ttk.Label(scrollable_frame, text="Tendencia de Ventas Semanales", 
                 style='Title.TLabel').pack(pady=(10, 5))
        
        for week, sales in trend_data['weekly_sales'].items():
            week_frame = ttk.Frame(scrollable_frame)
            week_frame.pack(fill=tk.X, padx=10, pady=2)
            
            ttk.Label(week_frame, text=f"Semana {week}", width=15).pack(side=tk.LEFT)
            
            # Barra de progreso para ventas
            max_sales = max(trend_data['weekly_sales'].values())
            progress = ttk.Progressbar(week_frame, length=200, 
                                      maximum=max_sales, value=sales)
            progress.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(week_frame, text=f"${sales:,.0f}").pack(side=tk.LEFT)
        
        # Insights predictivos
        ttk.Label(scrollable_frame, text="📊 Insights Predictivos", 
                 style='Title.TLabel').pack(pady=(20, 5))
        
        insight_frame = ttk.Frame(scrollable_frame)
        insight_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(insight_frame, text="Predicción próximo mes:").pack(anchor=tk.W)
        ttk.Label(insight_frame, text=f"${predictive['predicted_next_month']:,.2f}",
                 style='Metric.TLabel').pack(anchor=tk.W)
        ttk.Label(insight_frame, text=f"Confianza: {predictive['confidence']}",
                 style='Value.TLabel').pack(anchor=tk.W)

    def create_product_analysis(self, parent):
        """Análisis detallado de productos"""
        # Frame principal con scroll
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="📈 Análisis de Productos", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Métricas de productos
        product_metrics = self.analyzer.product_performance_metrics()
        
        # Frame para métricas principales
        metrics_frame = ttk.Frame(main_frame)
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Producto más vendido
        best_product = product_metrics.get('best_selling_product', 'N/A')
        ttk.Label(metrics_frame, text=f"🏆 Producto más vendido: {best_product}", 
                 font=('Arial', 12)).pack(pady=5)
        
        # Ranking de productos por revenue
        ranking_frame = ttk.LabelFrame(main_frame, text="Ranking de Productos por Ingresos")
        ranking_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview para mostrar el ranking
        tree = ttk.Treeview(ranking_frame, columns=('Producto', 'Ingresos', 'Unidades', 'Precio Promedio'), show='headings')
        
        # Configurar columnas
        tree.heading('Producto', text='Producto')
        tree.heading('Ingresos', text='Ingresos Total')
        tree.heading('Unidades', text='Unidades Vendidas')
        tree.heading('Precio Promedio', text='Precio Promedio')
        
        tree.column('Producto', width=150)
        tree.column('Ingresos', width=120)
        tree.column('Unidades', width=120)
        tree.column('Precio Promedio', width=120)
        
        # Agregar datos
        for product in product_metrics.get('rank_by_revenue', []):
            metrics = product_metrics['product_metrics'][product]
            tree.insert('', 'end', values=(
                product,
                f"${metrics['total_revenue']:,.2f}",
                metrics['units_sold'],
                f"${metrics['average_price']:,.2f}"
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(ranking_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_customer_analysis(self, parent):
        """Análisis de comportamiento del cliente"""
        customer_data = self.analyzer.customer_analysis()
        
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="👥 Análisis de Clientes", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Métricas principales
        metrics_frame = ttk.Frame(main_frame)
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)
        
        metrics = [
            ("Valor promedio por orden", f"${customer_data['average_order_value']:,.2f}"),
            ("Segmentos de cliente", f"{customer_data['customer_segments']}"),
            ("Cliente que más gasta", f"{customer_data['top_spending_segment'] or 'N/A'}"),
            ("Cliente más frecuente", f"{customer_data['most_frequent_segment'] or 'N/A'}")
        ]
        
        for title, value in metrics:
            metric_frame = ttk.Frame(metrics_frame)
            metric_frame.pack(fill=tk.X, pady=3)
            ttk.Label(metric_frame, text=title, width=20).pack(side=tk.LEFT)
            ttk.Label(metric_frame, text=value, style='Value.TLabel').pack(side=tk.RIGHT)

    def create_category_chart(self, parent):
        """Gráfico de ventas por categoría"""
        category_sales = self.analyzer.sales_by_category()
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="📊 Ventas por Categoría", 
                 style='Title.TLabel').pack(pady=10)
        
        # Crear gráfico de barras simple
        for category, sales in category_sales.items():
            category_frame = ttk.Frame(frame)
            category_frame.pack(fill=tk.X, padx=20, pady=5)
            
            ttk.Label(category_frame, text=category, width=15).pack(side=tk.LEFT)
            
            # Barra de progreso
            max_sales = max(category_sales.values())
            progress = ttk.Progressbar(category_frame, length=300, 
                                      maximum=max_sales, value=sales)
            progress.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(category_frame, text=f"${sales:,.2f}").pack(side=tk.LEFT)

    def create_product_chart(self, parent):
        """Gráfico de productos top"""
        top_products = self.analyzer.top_products(5)
        
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="🏆 Top 5 Productos", 
                 style='Title.TLabel').pack(pady=10)
        
        for product, sales in top_products.items():
            product_frame = ttk.Frame(frame)
            product_frame.pack(fill=tk.X, padx=20, pady=3)
            
            ttk.Label(product_frame, text=product, width=20).pack(side=tk.LEFT)
            
            # Barra de progreso
            max_sales = max(top_products.values())
            progress = ttk.Progressbar(product_frame, length=250, 
                                      maximum=max_sales, value=sales)
            progress.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(product_frame, text=f"${sales:,.2f}").pack(side=tk.LEFT)