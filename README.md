# megaline_telefonia
# 📊 Análisis de Tarifas de Megaline

Este proyecto simula una situación real de análisis de datos para la empresa de telecomunicaciones **Megaline**, la cual ofrece dos tarifas de prepago: `Surf` y `Ultimate`. El objetivo principal fue determinar cuál de estas tarifas genera más ingresos para ayudar a la empresa a enfocar mejor sus recursos publicitarios.

---

## 🎯 Objetivos del proyecto

- Analizar el comportamiento de los clientes según su plan (`Surf` o `Ultimate`).
- Estudiar llamadas, mensajes y consumo de datos móviles mensualmente.
- Calcular los ingresos mensuales generados por usuario.
- Comparar estadísticamente los ingresos por cada plan.
- Probar hipótesis estadísticas para validar si existen diferencias significativas.

---

## 🧰 Herramientas utilizadas

- Python 3.9
- pandas, numpy
- matplotlib, seaborn
- scipy.stats (para pruebas de hipótesis)
- Jupyter Notebook

---

## 🔍 Análisis realizado

- Carga y limpieza de datos desde múltiples archivos CSV.
- Transformación de fechas, eliminación de valores nulos y tipado correcto.
- Cálculo mensual del consumo de llamadas, mensajes y datos por usuario.
- Agrupación y fusión de los distintos DataFrames para obtener un panel por usuario/mes.
- Enriquecimiento con datos como ciudad, plan, meses de servicio.
- Visualización del comportamiento mensual de consumo por tipo de plan.
- Cálculo de ingresos excedentes y aplicación de reglas de facturación.
- Pruebas estadísticas (`Levene` y `t-test`) para comparar planes y regiones.

---

## 📈 Resultados clave

- Los usuarios del plan **Ultimate** generan ingresos constantes por su tarifa mensual más alta, pero rara vez exceden sus límites incluidos.
- Los usuarios del plan **Surf** superan más frecuentemente sus límites de datos, minutos y mensajes, lo que genera ingresos variables pero significativos.
- En diciembre, los usuarios de **Surf** llegaron a generar ingresos comparables o superiores a los de **Ultimate**.
- Las pruebas estadísticas confirmaron que **hay una diferencia significativa en los ingresos** generados por los dos planes.
- Sin embargo, **no hay evidencia estadística** para afirmar que los usuarios de NY/NJ generan ingresos distintos a los de otras regiones.

---

## ✅ Conclusiones


- Aunque **Ultimate** genera ingresos más estables por usuario, el crecimiento de ingresos en el plan **Surf** sugiere una oportunidad de optimización.
- Sería útil revisar qué está incentivando el mayor consumo en **Surf** y si puede replicarse en otras zonas o planes.
- Reconsiderar si el precio base de Ultimate justifica el gasto publicitario frente al comportamiento real de uso.

---

## 🔄 Posibles mejoras futuras

- Automatizar el pipeline de limpieza y análisis con scripts reutilizables.
- Incorporar análisis de abandono (`churn`) por plan y ciudad.
- Hacer dashboards interactivos con Streamlit o Power BI.
- Evaluar impacto de campañas de marketing cruzando con fechas relevantes.

