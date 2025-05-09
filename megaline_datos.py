#!/usr/bin/env python
# coding: utf-8




# # ¿Cuál es la mejor tarifa?
# 
# Trabajas como analista para el operador de telecomunicaciones Megaline. La empresa ofrece a sus clientes dos tarifas de prepago, Surf y Ultimate. El departamento comercial quiere saber cuál de las tarifas genera más ingresos para poder ajustar el presupuesto de publicidad.
# 
# Vas a realizar un análisis preliminar de las tarifas basado en una selección de clientes relativamente pequeña. Tendrás los datos de 500 clientes de Megaline: quiénes son los clientes, de dónde son, qué tarifa usan, así como la cantidad de llamadas que hicieron y los mensajes de texto que enviaron en 2018. Tu trabajo es analizar el comportamiento de los clientes y determinar qué tarifa de prepago genera más ingresos.

# [Te proporcionamos algunos comentarios para orientarte mientras completas este proyecto. Pero debes asegurarte de eliminar todos los comentarios entre corchetes antes de entregar tu proyecto.]
# 
# [Antes de sumergirte en el análisis de datos, explica por tu propia cuenta el propósito del proyecto y las acciones que planeas realizar.]
# 
# [Ten en cuenta que estudiar, modificar y analizar datos es un proceso iterativo. Es normal volver a los pasos anteriores y corregirlos/ampliarlos para permitir nuevos pasos.]



# ## Inicialización

# In[1]:


# Cargar todas las librerías
import pandas as pd
import numpy as np



# ## Cargar datos

# In[2]:


# Carga los archivos de datos en diferentes DataFrames
import pandas as pd
df_megaline_calls= pd.read_csv("/datasets/megaline_calls.csv")
df_megaline_internet = pd.read_csv("/datasets/megaline_internet.csv")
df_megaline_messages = pd.read_csv("/datasets/megaline_messages.csv")
df_megaline_plans = pd.read_csv("/datasets/megaline_plans.csv")
df_megaline_users = pd.read_csv("/datasets/megaline_users.csv")


# In[3]:


print("Información de df_megaline_calls:")
print(df_megaline_calls.info())

print("\nInformación de df_megaline_internet:")
print(df_megaline_internet.info())

print("\nInformación de df_megaline_messages:")
print(df_megaline_messages.info())

print("\nInformación de df_megaline_plans:")
print(df_megaline_plans.info())

print("\nInformación de df_megaline_users:")
print(df_megaline_users.info())


# In[4]:


print(df_megaline_calls.head())


# In[3]:


df_megaline_calls.describe()


# <div class="alert alert-block alert-warning">
# <b>Comentario adicional</b>
# Buena práctica al mostrar la información de cada DataFrame. Considera añadir df.describe() para obtener estadísticas resumidas de las variables numéricas.
# </div>

# ## Preparar los datos

# [Los datos para este proyecto se dividen en varias tablas. Explora cada una para tener una comprensión inicial de los datos. Si es necesario, haz las correcciones requeridas en cada tabla.]

# ## Tarifas

# In[5]:


# Imprime la información general/resumida sobre el DataFrame de las tarifas

print("Información resumida de df_megaline_planss:")
print(df_megaline_plans)


# In[6]:


# Imprime una muestra de los datos para las tarifas
df_megaline_plans



# In[ ]:



columns = [
    "messages_included",
    "mb_per_month_included",
    "minutes_included",
    "usd_monthly_pay",
    "usd_per_gb",
    "usd_per_message",
    "usd_per_minute",
    "plan_name"
]


columns = [col.replace("_", " ") for col in columns]

print(columns)





get_ipython().run_line_magic('pinfo', 'replace')


# ## Enriquecer los datos


# In[17]:


# Mover "plan_name" a la primera posición
df_megaline_plans.insert(0, 'plan_name', df_megaline_plans.pop('plan_name'))

# Imprimir el DataFrame para verificar el cambio
print(df_megaline_plans)


# In[18]:


#agregar una columna que contenga los gb incluidos
df_megaline_plans['internet_included'] = df_megaline_plans['mb_per_month_included'] / 1024
# Cambia el tipo de dato de la columna 'internet_included' a 'int64'
df_megaline_plans['internet_included'] = df_megaline_plans['internet_included'].astype('int64')


# ## Usuarios/as

# In[4]:


# Imprime la información general/resumida sobre el DataFrame de usuarios

print("Información resumida de df_megaline_users:")
print(df_megaline_users)


# In[10]:


# Imprime una muestra de datos para usuarios

df_megaline_users


# De igual forma en el siguiente DF se puede observar en el nombre de las columnas que hay nombres con guiones bajos y también hay elementos ausentes

# ### Corregir los datos


# In[20]:


columns = [
    "user_id",
    "first_name",
    "last_name",
    "reg_date",
    "churn_date"
    
]


columns = [col.replace("_", " ") for col in columns]

print(columns)


# In[22]:


# Cambiar los tipo de datos de `reg_date` a tipo `datetime`
df_megaline_users['reg_date'] = pd.to_datetime(df_megaline_users['reg_date'], format='%Y-%m-%d')
# Cambiar los tipos de datos de 'churn_date' que no son nulos a tipo 'datetime'
df_megaline_users['churn_date'] = pd.to_datetime(df_megaline_users['churn_date'], format='%Y-%m-%d')


# ### Enriquecer los datos


# In[12]:


print(df_megaline_users.isna().sum()) #se buscaron valores ausentes


# In[9]:


print(df_megaline_users.fillna(value="")) # se reemplazaron los valores ausentes


# In[14]:


df_megaline_users["reg_date"] = pd.to_datetime(df_megaline_users["reg_date"])

# Extraer el mes y añadirlo como una nueva columna
df_megaline_users["month"] = df_megaline_users["reg_date"].dt.month

# Mostrar las primeras filas para verificar
print(df_megaline_users.head())


# In[10]:


df_megaline_users.describe()


# In[24]:


# Crear una función que calcule los meses de servicio que ha tenido cada usuario
def calc_service_months(user):
    """
    evalúar si el usuario sigue activo o dejó el servicio y posteriormente calcúla los meses de servicio.
    """
    if pd.isnull(user['leave_date']):
            months = 13 - (user['reg_month'])
    else:
            months = (user['leave_date']) - user['reg_month'] + 1
    return months


# In[27]:


# Agregar una columnasi el usuario está en la zona de NY o NJ
df_megaline_users['isin_ny_nj'] = df_megaline_users['city'].str.contains('NY|NJ')
# Añade una columna con el mes en el que el usuario se registró.
df_megaline_users['reg_month'] = df_megaline_users['reg_date'].dt.month
# Añade una columna con el mes en que el usuario dejó de usar el servicio.
df_megaline_users['leave_date'] = df_megaline_users['churn_date'].dt.month
# Añade una columna con la cantidad de meses de servicio.
df_megaline_users['service_months'] = df_megaline_users.apply(calc_service_months, axis=1)


# ## Llamadas

# In[11]:


# Imprime la información general/resumida sobre el DataFrame de las llamadas

print("Información de df_megaline_calls:")
print(df_megaline_calls.info())


# In[16]:


# Imprime una muestra de datos para las llamadas
df_megaline_calls



# ### Corregir los datos

# se reemplazaran los valores de las columnas con guíon bajo

# In[12]:


columns = [
    "user_id",
    "call_date"   
]


columns = [col.replace("_", " ") for col in columns]

print(columns)


# In[31]:


# Eliminar las llamadas que duraron 0.0
df_megaline_calls = df_megaline_calls[~(df_megaline_calls['duration']==0)]
# Cambia la columna 'call_date' a 'datetime'
df_megaline_calls['call_date'] = pd.to_datetime(df_megaline_calls['call_date'], format='%Y-%m-%d')
# Redondea las cifras de 'duration' hacia arriba.
df_megaline_calls['duration'] = np.ceil(df_megaline_calls['duration'])
# # Cambia el tipo de dato de la columna 'duration' a tipo 'int'
df_megaline_calls['duration'] = df_megaline_calls['duration'].astype('int64')


# In[32]:


# Agrega la columna 'plan' a la variable 'data_calls
df_megaline_calls = df_megaline_calls.set_index('user_id').join(df_megaline_calls[['user_id', 'plan']].set_index('user_id'))
# Resetea el índice
df_megaline_calls = df_megaline_calls.reset_index()



# In[13]:


#se agregan los datos de month
df_megaline_calls["call_date"] = pd.to_datetime(df_megaline_calls["call_date"])

# Extraer el mes y añadirlo como una nueva columna
df_megaline_calls["month"] = df_megaline_calls["call_date"].dt.month

# Mostrar las primeras filas para verificar
print(df_megaline_calls.head())


# In[28]:


# Revisar la distribución de la columna 'duration'
print(df_megaline_calls['duration'].describe())


# ## Mensajes

# In[14]:


# Imprime la información general/resumida sobre el DataFrame de los mensajes

df_megaline_messages = pd.read_csv("/datasets/megaline_messages.csv")
print(df_megaline_messages.info())


# In[20]:


# Imprime una muestra de datos para los mensajes

df_megaline_messages


# [Describe lo que ves y observas en la información general y en la muestra de datos impresa para el precio de datos anterior. ¿Hay algún problema (tipos de datos no adecuados, datos ausentes, etc.) que pudieran necesitar investigación y cambios adicionales? ¿Cómo se puede arreglar?]

# ### Corregir los datos

# [Corrige los problemas obvios con los datos basándote en las observaciones iniciales.]

# In[15]:


columns = [
    "user_id",
    "message_date"   
]


columns = [col.replace("_", " ") for col in columns]

print(columns)


# In[33]:


# Cambiar la columna 'message_date' a tipo 'datetime'
df_megaline_messages['message_date'] = pd.to_datetime(df_megaline_messages['message_date'], format='%Y-%m-%d')



df_megaline_messages["message_date"] = pd.to_datetime(df_megaline_messages["message_date"])

# Extraer el mes y añadirlo como una nueva columna
df_megaline_messages["month"] = df_megaline_messages["message_date"].dt.month

# Mostrar las primeras filas para verificar
print(df_megaline_messages.head())


# ## Internet

# In[23]:


# Imprime la información general/resumida sobre el DataFrame de internet

print("\nInformación de df_megaline_internet:")
print(df_megaline_internet.info())


# In[24]:


# Imprime una muestra de datos para el tráfico de internet

df_megaline_internet




columns = [
    "user_id",
    "session_date",
    "mb_used"
]


columns = [col.replace("_", " ") for col in columns]

print(columns)


# In[34]:


# Cambia el tipo de dato de la columna 'session_date' a tipo 'datetime'
df_megaline_internet['session_date'] = pd.to_datetime(df_megaline_internet['session_date'], format='%Y-%m-%d')



# In[26]:


df_megaline_internet["session_date"] = pd.to_datetime(df_megaline_internet["session_date"])

# Extraer el mes y añadirlo como una nueva columna
df_megaline_internet["month"] = df_megaline_internet["session_date"].dt.month

# Mostrar las primeras filas para verificar
print(df_megaline_internet.head())



# Imprime las condiciones de la tarifa y asegúrate de que te quedan claras

df_megaline_plans[["plan_name","usd_monthly_pay"]]


# In[28]:


df_megaline_calls





# Calcula el número de llamadas hechas por cada usuario al mes. Guarda el resultado.

number_calls = df_megaline_calls.groupby('user_id')["call_date"].count()
print(number_calls)
#se puede ver el número de llamadas hechas por cada usuario agrupando en un filtrado del dataframe por nombre de usuario y con la suma de numero de veces de llamadas por duracion


# In[30]:


# Calcula la cantidad de minutos usados por cada usuario al mes. Guarda el resultado.

minutes_calls = df_megaline_calls.groupby('user_id')["duration"].sum()
print(minutes_calls)


# In[31]:


# Calcula el número de mensajes enviados por cada usuario al mes. Guarda el resultado.

messages_calls = df_megaline_messages.groupby('user_id')["message_date"].count()
print(messages_calls)


# In[32]:


# Calcula el volumen del tráfico de Internet usado por cada usuario al mes. Guarda el resultado.

trafic_internet = df_megaline_internet.groupby('user_id')['mb_used'].count()
print(trafic_internet)


# [Junta los datos agregados en un DataFrame para que haya un registro que represente lo que consumió un usuario único en un mes determinado.]

# In[33]:


df_megaline_users[set(df_megaline_calls.columns) & set(df_megaline_users.columns)]


# In[34]:


#fusiona los datos de llamadas, internet y mensajes en "user_id" y "mounth"
df_full = df_megaline_users.set_index(["user_id", "month"])\
    .join(df_megaline_calls.groupby(["user_id", "month"])["duration"].sum().rename("total_duration"))\
    .join(df_megaline_messages.groupby(["user_id", "month"]).size().rename("n_messages"))\
    .join(df_megaline_internet.groupby(["user_id", "month"]).size().rename("n_internet"))
          
print(df_full)


# In[35]:


df_full


# In[38]:


df_megaline_plans


# In[41]:


# Añade la información de la tarifa

# Añade la columna del plan que tiene cada usuario y si se encuentra el la zona de New York o New Jersey
total_consume_user_month = df_megaline_plans.join(df_megaline_plans[['user_id', 'plan', 'isin_ny_nj']].set_index('user_id'))
# Añade a cada usuario la información del plan que tiene
total_consume_user_month = total_consume_user_month.join(df_megaline_plans.set_index('plan_name'), on='plan')


# [Calcula los ingresos mensuales por usuario (resta el límite del paquete gratuito del número total de llamadas, mensajes de texto y datos; multiplica el resultado por el valor del plan de llamadas; añade la tarifa mensual en función del plan de llamadas). Nota: Dadas las condiciones del plan, ¡esto podría no ser tan trivial como un par de líneas! Así que no pasa nada si dedicas algo de tiempo a ello.]

# In[40]:


df_full


# In[42]:


def calc_income(user):
    if user['plan'] == 'surf':
        if (user['minutes_included']<user['tot_duration']):
            # user['column_1'] = abs((user['minutes_included'] - user['tot_duration']) * 0.03)
            num1 = abs((user['minutes_included'] - user['tot_duration']) * 0.03)
        else:
            num1 = 0
        if (user['messages_included']<user['num_messages']):
            num2 = abs((user['messages_included'] - user['num_messages']) * 0.03)
        else:
            num2 = 0
        if (user['internet_included']<user['gb_used_month']):
            num3 = abs((user['internet_included'] - user['gb_used_month']) * 10)
        else:
            num3 = 0
    else:
        if (user['minutes_included']<user['tot_duration']):
            num1 = abs((user['minutes_included'] - user['tot_duration']) * 0.01)
        else:
            num1 = 0

        if (user['messages_included']<user['num_messages']):
            num2 = abs((user['messages_included'] - user['num_messages']) * 0.01)
        else:
            num2 = 0

        if (user['internet_included']<user['gb_used_month']):
            num3 = abs((user['internet_included'] - user['gb_used_month']) * 7)
        else:
            num3 = 0
    return num1, num2, num3




# ## Estudia el comportamiento de usuario

# [Calcula algunas estadísticas descriptivas para los datos agregados y fusionados que nos sean útiles y que muestren un panorama general captado por los datos. Dibuja gráficos útiles para facilitar la comprensión. Dado que la tarea principal es comparar las tarifas y decidir cuál es más rentable, las estadísticas y gráficas deben calcularse por tarifa.]
# 
# [En los comentarios hallarás pistas relevantes para las llamadas, pero no las hay para los mensajes e Internet. Sin embargo, el principio del estudio estadístico que se aplica para ellos es el mismo que para las llamadas.]

# ### Llamadas

# In[41]:


# Compara la duración promedio de llamadas por cada plan y por cada mes. Traza un gráfico de barras para visualizarla.

import pandas as pd
import matplotlib.pyplot as plt

average_duration = df_full.groupby(['plan', 'month'])['total_duration'].mean().reset_index()

print(average_duration)

plt.figure(figsize=(12, 8))

pivot_table = average_duration.pivot(index='month', columns='plan', values='total_duration')


pivot_table.plot(kind='bar', figsize=(12, 8), width=0.8)


plt.title('Duración Promedio de Llamadas por Plan y Mes')
plt.xlabel('Mes')
plt.ylabel('Duración Promedio de Llamadas (en minutos)')
plt.legend(title='Plan')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()


# In[42]:


# Compara el número de minutos mensuales que necesitan los usuarios de cada plan. Traza un histograma.

monthly_minutes = df_full.groupby(['plan', 'month'])['total_duration'].sum().reset_index()

print(monthly_minutes.head())

plt.figure(figsize=(12, 8))


for plan in monthly_minutes['plan'].unique():
    
    data = monthly_minutes[monthly_minutes['plan'] == plan]['total_duration']
    plt.hist(data, bins=20, alpha=0.5, label=f'Plan {plan}')


plt.title('Distribución del Número de Minutos Mensuales por Plan')
plt.xlabel('Número de Minutos Mensuales')
plt.ylabel('Frecuencia')
plt.legend(title='Plan')
plt.grid(True)
plt.tight_layout()


plt.show()


# [Calcula la media y la variable de la duración de las llamadas para averiguar si los usuarios de los distintos planes se comportan de forma diferente al realizar sus llamadas.]

# In[43]:


# Calcula la media y la varianza de la duración mensual de llamadas.

monthly_duration = df_full.groupby('month')['total_duration'].sum().reset_index()

# Calcular la media y la varianza de la duración mensual de llamadas
mean_duration = monthly_duration['total_duration'].mean()
variance_duration = monthly_duration['total_duration'].var()

print(f'Media de la duración mensual de llamadas: {mean_duration:.2f} minutos')
print(f'Varianza de la duración mensual de llamadas: {variance_duration:.2f} minutos^2')



# In[44]:


# Traza un diagrama de caja para visualizar la distribución de la duración mensual de llamadas

import seaborn as sns


# Agrupar por mes y calcular la suma total de duración de llamadas por mes
monthly_duration = df_full.groupby('month')['total_duration'].sum().reset_index()

# Configurar el estilo de los gráficos con seaborn
sns.set(style="whitegrid")

# Crear el gráfico de caja
plt.figure(figsize=(12, 8))
sns.boxplot(x='month', y='total_duration', data=monthly_duration)



# In[45]:


# Comprara el número de mensajes que tienden a enviar cada mes los usuarios de cada plan

import seaborn as sns


monthly_messages = df_full.groupby(['plan', 'month'])['n_messages'].sum().reset_index()

print(monthly_messages.head())


# In[46]:


# Compara la cantidad de tráfico de Internet consumido por usuarios por plan

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Agrupar por plan y calcular la suma total de tráfico de Internet por mes
monthly_internet = df_full.groupby(['plan', 'month'])['n_internet'].sum().reset_index()

print(monthly_internet.head())

plt.figure(figsize=(12, 8))
sns.barplot(data=monthly_internet, x='month', y='n_internet', hue='plan', palette='viridis')

# Personalizar el gráfico
plt.title('Tráfico de Internet Consumido por Mes por Plan')
plt.xlabel('Mes')
plt.ylabel('Cantidad de Tráfico de Internet (en MB o GB)')
plt.xticks(rotation=45)
plt.legend(title='Plan')
plt.grid(True)
plt.tight_layout()

# Mostrar el gráfico
plt.show()


# In[ ]:


#se puede observar que hay más tráfico de internet por mes en el plan surf, hay un cambio notable desde el segundo mes 


# [Elabora las conclusiones sobre el comportamiento de los usuarios con respecto a los mensajes. ¿Su comportamiento varía en función del plan?]

# ### Internet

# In[ ]:


en promedio los usuarios del plan 'ultimate' utiliza más sus mensajes que los usuarios de 'surf', 


# In[ ]:


los usuarios del plan "ultimate" en promedio no llega a gastar sus Gb incluidos, lo que podría indicar que los usuarios de "surf" dejan más ingresos por pagar Gb extra cada mes


# In[ ]:


en el caso de "surf" la mediana indica que por lo menos la mitad de usuarios gastan al rededor de 17 Gb y sólo se le incluyen 15 en su plan. Lo que podría indicar que dejan buena cantidad de ingresos.


# [Elabora las conclusiones sobre cómo los usuarios tienden a consumir el tráfico de Internet. ¿Su comportamiento varía en función del plan?]

# ## Ingreso

# [Del mismo modo que has estudiado el comportamiento de los usuarios, describe estadísticamente los ingresos de los planes.]

# In[ ]:


parece ser que aún cuando lo usuarios de "surf" dejan buenos ingresos al exceder sus Gb incluídos, los usuarios del plan "ultimate" por lo regular no exceden su plan


# In[ ]:


al no llegar a su límite incluido, constantemente dejan los mismos ingresos, que son mayores a los de los ususarios de "surf".


# In[ ]:





# [Elabora las conclusiones sobre cómo difiere el ingreso entre los planes.]

# 

# ## Prueba las hipótesis estadísticas

# [Prueba la hipótesis de que son diferentes los ingresos promedio procedentes de los usuarios de los planes de llamada Ultimate y Surf.]

# [Elabora las hipótesis nula y alternativa, escoge la prueba estadística, determina el valor alfa.]

# In[ ]:


df_full


# In[36]:


def levene_test(s1, s2, center='mean'):
    levene = st.levene(s1, s2, center=center)
    return levene


# In[37]:


# Crea variables para guardar las muestras de los usuarios que vamos a comparar.
mean_income_users_surf = df_full.query('plan=="surf"')['total_monthly_income']
mean_income_users_ultimate = df_full.query('plan=="ultimate"')['total_monthly_income']
# Aplicar la prueba de Levene para ver la igualdad de varianzas de nuestras muestras.
levene_test_plans = levene_test(mean_income_users_surf, mean_income_users_ultimate)
print(f'p-value de la prueba Levene: {levene_test_plans.pvalue}')
# Prueba la hipótesis
alpha = 0.05
if levene_test_plans.pvalue < alpha:
    equal_var = False
else:
    equal_var = True
results = st.ttest_ind(mean_income_users_surf, mean_income_users_ultimate, equal_var=equal_var)
print('p-value de la prueba T:', results.pvalue)
if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula, generan diferentes ingresos.")
else:
    print("No rechazamos la hipótesis nula, generan iguales ingresos.")


# [Prueba la hipótesis de que el ingreso promedio de los usuarios del área NY-NJ es diferente al de los usuarios de otras regiones.]

# [Elabora las hipótesis nula y alternativa, escoge la prueba estadística, determina el valor alfa.]

# In[39]:


# Crea variables para guardar las muestras de las áreas que vamos a comparar.
ny_nj_mean_income = df_full.query('isin_ny_nj == True')['total_monthly_income']
rest_mean = df_full.query('isin_ny_nj == False')['total_monthly_income']
# Aplicar la prueva de Levene para ver la igualdad de varianzas de nuestras muestras.
levene_test_area = levene_test(ny_nj_mean_income, rest_mean)
print(f'p-value de la prueba Levene: {levene_test_area.pvalue}')
# Prueba la hipótesis
alpha = 0.05
if levene_test_area.pvalue < alpha:
    equal_var = False
else:
    equal_var = True
results = st.ttest_ind(ny_nj_mean_income, rest_mean, equal_var=equal_var)
print('p-value de la prueba T:', results.pvalue)
if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula, generan diferentes ingresos.")
else:
    print("No rechazamos la hipótesis nula, generan iguales ingresos.")


# ## Conclusión general
# 


# In[ ]:


La distribución de las llamadas de los usuarios de cada plan indica que los usuarios del plan 'surf' excede en cierta medida su límite de mínutos incluídos, lo que significa algunos ingresos extra por exceder su límite.
En la investigación de los mensajes observamos una situación similar, tenemos ingresos extra por usuarios que exceden el límite de sus mensajes.
Para el tráfico de datos, se observa que los usuarios del plan 'surf' al igual que en mensajes y llamadas dejan ingresos extra, sin embargo, en este apartado, el promedio de datos que utilizan los usuarios de este plan supera los datos incluidos en su plan, por lo cual son considerables los ingresos extra, teniendo en cuenta que hay más usarios del plan 'surf'.
En la investigación de los ingresos de los usuarios de cada plan, en promedio, los usuarios del plan 'ultimate' dejan más ingresos, sin embargo, en el último mes (Diciembre), los ingresos promedio de los ususarios del plan 'surf' alcanzaron USD $70, además, si observamos la suma de ingresos de los usuarios del plan 'surf' aumentaron considerablemente a lo largo del año, en comparación de los ingresos de los usuarios del plan 'ultimate', situación que se observa en los gráficos de los minutos, mensajes y Gb usados en cada plan, razón por la cual sería conveniente revisar qué se está haciendo bien en el plan 'surf'.
Al realizar la prueba de hipótesis estadística comprobamos que los ingresos son diferentes en los usuarios de cada plan, que confirma lo antes observado en los gráficos, lo que da pie a ponerle más atención al plan 'surf'
En cuanto a los ingresos de los usuarios del área de New York y New Jersey, observamos que nuestra hipotésis estadística indica que no podemos rechazar que los usuarios de esa área generan ingresos diferentes al resto de usuarios, entonces lo que se observa en el boxplot de la distribución de ingresos de ambas áreas, puede ser que los valores atípicos den una lectura errónea de los ingresos.


# In[ ]:




