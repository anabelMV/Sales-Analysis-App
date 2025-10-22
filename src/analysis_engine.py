import csv
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import logging

class SalesAnalyzer:
    def __init__(self, data_path='data/sample_sales.csv'):
        self.logger = self.setup_logger()
        self.data = self.load_data(data_path)
    
    def setup_logger(self):
        """Sistema de logging profesional - debe ir PRIMERO"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sales_analysis.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_data(self, data_path):
        """Cargar datos desde CSV"""
        data = []
        try:
            with open(data_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Convertir tipos de datos
                    row['quantity'] = int(row['quantity'])
                    row['unit_price'] = float(row['unit_price'])
                    row['total_sale'] = float(row['total_sale'])
                    data.append(row)
            
            self.logger.info(f"Datos cargados: {len(data)} registros desde {data_path}")
            return data
            
        except FileNotFoundError:
            self.logger.error(f"Archivo no encontrado: {data_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")
            raise
    
    
    def get_summary_stats(self):
        """Estadísticas resumen de las ventas"""
        total_sales = sum(record['total_sale'] for record in self.data)
        total_orders = len(self.data)
        avg_sale = total_sales / total_orders if total_orders > 0 else 0
        
        # Encontrar rango de fechas
        dates = [datetime.strptime(record['sale_date'], '%Y-%m-%d') for record in self.data]
        min_date = min(dates)
        max_date = max(dates)
        
        # Calcular ventas de hoy (simulado)
        today = datetime.now().date()
        sales_today = sum(
            record['total_sale'] for record in self.data 
            if datetime.strptime(record['sale_date'], '%Y-%m-%d').date() == today
        )
        
        return {
            'total_sales': total_sales,
            'average_sale': avg_sale,
            'total_orders': total_orders,
            'date_range': f"{min_date.date()} to {max_date.date()}",
            'sales_today': sales_today
        }
    
    def sales_by_category(self):
        """Ventas por categoría"""
        category_sales = defaultdict(float)
        for record in self.data:
            # Determinar categoría basada en el producto
            product = record['product']
            if product in ['Laptop', 'Tablet', 'Smartphone', 'Monitor']:
                category = 'Electrónicos'
            elif product in ['Mouse', 'Teclado', 'Auriculares']:
                category = 'Accesorios'
            else:
                category = 'Dispositivos'
            
            category_sales[category] += record['total_sale']
        
        # Ordenar de mayor a menor
        return dict(sorted(category_sales.items(), key=lambda x: x[1], reverse=True))
    
    def top_products(self, n=5):
        """Top N productos por ventas"""
        product_sales = defaultdict(float)
        for record in self.data:
            product_sales[record['product']] += record['total_sale']
        
        # Ordenar y tomar top N
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_products[:n])
    
    def regional_analysis(self):
        """Análisis por región"""
        region_sales = defaultdict(float)
        for record in self.data:
            region_sales[record['region']] += record['total_sale']
        
        return dict(sorted(region_sales.items(), key=lambda x: x[1], reverse=True))
    
    def sales_trend_analysis(self):
        """Análisis de tendencias y crecimiento"""
        # Agrupar ventas por semana
        weekly_sales = defaultdict(float)
        for record in self.data:
            sale_date = datetime.strptime(record['sale_date'], '%Y-%m-%d')
            week_key = sale_date.strftime('%Y-%U')  # Año-Semana
            weekly_sales[week_key] += record['total_sale']
        
        # Calcular crecimiento semanal
        weeks = sorted(weekly_sales.keys())
        growth_rates = []
        for i in range(1, len(weeks)):
            current = weekly_sales[weeks[i]]
            previous = weekly_sales[weeks[i-1]]
            growth = ((current - previous) / previous * 100) if previous > 0 else 0
            growth_rates.append(growth)
        
        avg_growth = statistics.mean(growth_rates) if growth_rates else 0
        
        return {
            'weekly_sales': dict(weekly_sales),
            'average_weekly_growth': round(avg_growth, 2),
            'total_weeks': len(weeks),
            'best_week': max(weekly_sales, key=weekly_sales.get) if weekly_sales else None,
            'worst_week': min(weekly_sales, key=weekly_sales.get) if weekly_sales else None
        }
    
    def customer_analysis(self):
        """Análisis de comportamiento del cliente"""
        customer_spending = defaultdict(float)
        customer_frequency = defaultdict(int)
        
        for record in self.data:
            # Usamos región + tipo como "cliente" para este ejemplo
            customer_key = f"{record['region']}_{record['customer_type']}"
            customer_spending[customer_key] += record['total_sale']
            customer_frequency[customer_key] += 1
        
        # Calcular métricas de cliente
        if customer_spending:
            avg_order_value = statistics.mean(customer_spending.values())
            max_spender = max(customer_spending, key=customer_spending.get)
            most_frequent = max(customer_frequency, key=customer_frequency.get)
        else:
            avg_order_value = 0
            max_spender = None
            most_frequent = None
        
        return {
            'average_order_value': round(avg_order_value, 2),
            'top_spending_segment': max_spender,
            'most_frequent_segment': most_frequent,
            'customer_segments': len(customer_spending),
            'total_customers': sum(customer_frequency.values())
        }
    
    def product_performance_metrics(self):
        """Métricas avanzadas de desempeño de productos"""
        product_metrics = {}
        
        for product in set(record['product'] for record in self.data):
            product_sales = [r for r in self.data if r['product'] == product]
            
            if product_sales:
                total_revenue = sum(r['total_sale'] for r in product_sales)
                total_units = sum(r['quantity'] for r in product_sales)
                avg_price = statistics.mean(r['unit_price'] for r in product_sales)
                
                product_metrics[product] = {
                    'total_revenue': round(total_revenue, 2),
                    'units_sold': total_units,
                    'average_price': round(avg_price, 2),
                    'total_orders': len(product_sales),
                    'revenue_per_order': round(total_revenue / len(product_sales), 2)
                }
        
        # Rankings
        sorted_by_revenue = sorted(product_metrics.items(), 
                                 key=lambda x: x[1]['total_revenue'], reverse=True)
        
        return {
            'product_metrics': product_metrics,
            'rank_by_revenue': [item[0] for item in sorted_by_revenue],
            'best_selling_product': sorted_by_revenue[0][0] if sorted_by_revenue else None
        }
    
    def predictive_insights(self):
        """Insights predictivos simples"""
        # Análisis de estacionalidad básico
        monthly_sales = defaultdict(float)
        for record in self.data:
            sale_date = datetime.strptime(record['sale_date'], '%Y-%m-%d')
            month_key = sale_date.strftime('%Y-%m')
            monthly_sales[month_key] += record['total_sale']
        
        # Predecir próximo mes (promedio simple)
        if len(monthly_sales) >= 2:
            last_months = list(monthly_sales.values())[-3:]  # Últimos 3 meses
            predicted_next = statistics.mean(last_months)
            confidence = 'high' if len(monthly_sales) >= 3 else 'medium'
        else:
            predicted_next = sum(monthly_sales.values()) / len(monthly_sales) if monthly_sales else 0
            confidence = 'low'
        
        return {
            'monthly_trend': dict(monthly_sales),
            'predicted_next_month': round(predicted_next, 2),
            'confidence': confidence
        }