import csv
import random
from datetime import datetime, timedelta
import os

def generate_sales_data(num_records=2000):
    """Genera datos de ventas sintéticos SIN PANDAS"""
    
    products = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Tablet', 'Smartphone', 'Auriculares', 'Impresora']
    categories = ['Electrónicos', 'Accesorios', 'Dispositivos']
    regions = ['Norte', 'Sur', 'Este', 'Oeste']
    customer_types = ['Individual', 'Empresa', 'Gobierno']
    
    # Generar fechas de los últimos 90 días
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    data = []
    for i in range(num_records):
        product = random.choice(products)
        category = 'Electrónicos' if product in ['Laptop', 'Tablet', 'Smartphone'] else 'Accesorios'
        unit_price = random.uniform(50, 1500)
        quantity = random.randint(1, 5)
        total_sale = unit_price * quantity
        
        # Fecha aleatoria en el rango
        days_diff = random.randint(0, 89)
        sale_date = start_date + timedelta(days=days_diff)
        
        record = {
            'order_id': f'ORD_{1000 + i}',
            'product': product,
            'category': category,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'sale_date': sale_date.strftime('%Y-%m-%d'),
            'region': random.choice(regions),
            'customer_type': random.choice(customer_types),
            'total_sale': round(total_sale, 2)
        }
        data.append(record)
    
    # Guardar como CSV
    os.makedirs('data', exist_ok=True)
    with open('data/sample_sales.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['order_id', 'product', 'category', 'quantity', 'unit_price', 
                     'sale_date', 'region', 'customer_type', 'total_sale']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    # Mostrar resumen
    total_sales = sum(record['total_sale'] for record in data)
    unique_products = len(set(record['product'] for record in data))
    
    print("🔄 Generando datos de ventas sintéticos...")
    print(f"✅ Datos generados: {len(data)} registros guardados en data/sample_sales.csv")
    print(f"📊 Resumen:")
    print(f"   - Productos: {unique_products}")
    print(f"   - Ventas totales: ${total_sales:,.2f}")
    print(f"   - Período: {start_date.date()} a {end_date.date()}")
    
    return data

if __name__ == "__main__":
    generate_sales_data(2000)