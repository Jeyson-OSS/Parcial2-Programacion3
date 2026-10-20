import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit
)

class AplicacionInventario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Consultoría de Inventario - UGB")
        self.setGeometry(100, 100, 1050, 650)
        
        # 1. Cargar e inspeccionar los datos con Pandas
        self.df = pd.read_csv('inventario_datos.csv')
        
        self.initUI()
        
    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout_principal = QHBoxLayout(main_widget)
        
        # --- PANEL IZQUIERDO: Tabla y Análisis de Pandas ---
        panel_izquierdo = QVBoxLayout()
        
        label_tabla = QLabel("<b>Inventario General (Datos Registrados)</b>")
        panel_izquierdo.addWidget(label_tabla)
        
        # Tabla en la interfaz
        self.tabla = QTableWidget()
        self.cargar_tabla()
        panel_izquierdo.addWidget(self.tabla)
        
        # Inspección y estadísticas básicas con Pandas
        label_resumen = QLabel("<b>Análisis Estructural y Estadísticas con Pandas:</b>")
        panel_izquierdo.addWidget(label_resumen)
        
        self.txt_resumen = QTextEdit()
        self.txt_resumen.setReadOnly(True)
        self.mostrar_inspeccion_pandas()
        panel_izquierdo.addWidget(self.txt_resumen)
        
        layout_principal.addLayout(panel_izquierdo, stretch=3)
        
        # --- PANEL DERECHO: Visualización con Matplotlib ---
        panel_derecho = QVBoxLayout()
        
        label_grafico = QLabel("<b>Visualización Gráfica de Datos</b>")
        panel_derecho.addWidget(label_grafico)
        
        # Figura de Matplotlib
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        panel_derecho.addWidget(self.canvas)
        
        # Botones para alternar gráficos
        btn_sucursal = QPushButton("Ver Stock por Sucursal")
        btn_sucursal.clicked.connect(self.graficar_sucursal)
        panel_derecho.addWidget(btn_sucursal)
        
        btn_categoria = QPushButton("Ver Distribución por Categoría")
        btn_categoria.clicked.connect(self.graficar_categoria)
        panel_derecho.addWidget(btn_categoria)
        
        layout_principal.addLayout(panel_derecho, stretch=2)
        
        # Cargar gráfico inicial
        self.graficar_sucursal()

    def cargar_tabla(self):
        """Carga el CSV en la tabla visual de PyQt5"""
        self.tabla.setRowCount(len(self.df))
        self.tabla.setColumnCount(len(self.df.columns))
        self.tabla.setHorizontalHeaderLabels(self.df.columns)
        
        for row in range(len(self.df)):
            for col in range(len(self.df.columns)):
                item = QTableWidgetItem(str(self.df.iloc[row, col]))
                self.tabla.setItem(row, col, item)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def mostrar_inspeccion_pandas(self):
        """Genera el análisis e inspección solicitado"""
        total_stock = self.df['Cantidad_Stock'].sum()
        promedio_precio = self.df['Precio_Unitario'].mean()
        por_sucursal = self.df.groupby('Sucursal')['Cantidad_Stock'].sum()
        
        resumen = f"• Registros analizados: {len(self.df)}\n"
        resumen += f"• Unidades totales en stock: {total_stock}\n"
        resumen += f"• Precio promedio unitario: ${promedio_precio:.2f}\n\n"
        resumen += "• Stock acumulado por sucursal:\n"
        for suc, cant in por_sucursal.items():
            resumen += f"   - {suc}: {cant} unidades\n"
            
        self.txt_resumen.setText(resumen)

    def graficar_sucursal(self):
        """Genera gráfico de barras con Matplotlib"""
        self.ax.clear()
        datos_sucursal = self.df.groupby('Sucursal')['Cantidad_Stock'].sum()
        datos_sucursal.plot(kind='bar', ax=self.ax, color='#1f77b4')
        self.ax.set_title("Stock Total por Sucursal")
        self.ax.set_ylabel("Cantidad en Stock")
        self.ax.set_xlabel("Sucursales")
        plt.xticks(rotation=30, ha='right')
        self.figure.tight_layout()
        self.canvas.draw()

    def graficar_categoria(self):
        """Genera gráfico circular con Matplotlib"""
        self.ax.clear()
        datos_cat = self.df.groupby('Categoria')['Cantidad_Stock'].sum()
        datos_cat.plot(kind='pie', ax=self.ax, autopct='%1.1f%%', startangle=90)
        self.ax.set_title("Distribución por Categoría")
        self.ax.set_ylabel("")
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AplicacionInventario()
    ventana.show()
    sys.exit(app.exec_())