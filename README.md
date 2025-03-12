#Cración de entorno virtual 
python -m venv venv
venv\Scripts\activate #Windows

#Instalación de dependencias
pip install -r requirements.txt

#Configuración de la base de datos y sincronización
flask db init
flask db migrate -m "Inicialización de la base de datos"
flask db upgrade
