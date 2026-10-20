import pandas as pd
import random

sucursales = ['San Salvador', 'Santa Ana', 'San Miguel', 'La Libertad', 'Sonsonate']
categorias = {
    'Electrónica': ['Televisor', 'Laptop', 'Smartphone'],
    'Electrodomésticos': ['Refrigeradora', 'Microondas', 'Licuadora'],
    'Muebles': ['Sofá', 'Comedor', 'Cama']
}

datos = []
for i in range(1, 101):
    categoria = random.choice(list(categorias.keys()))
    producto = random.choice(categorias[categoria])
    sucursal = random.choice(sucursales)
    precio = round(random.uniform(15.0, 800.0), 2)
    cantidad = random.randint(0, 50)
    datos.append([f'PRD-{i:03d}', producto, categoria, sucursal, precio, cantidad])

df_inventario = pd.DataFrame(datos, columns=['ID_Producto', 'Producto', 'Categoria', 'Sucursal', 'Precio_Unitario', 'Cantidad_Stock'])
df_inventario.to_csv('inventario_datos.csv', index=False)
print("Archivo generado con éxito.")