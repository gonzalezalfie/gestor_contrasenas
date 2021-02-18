## Cómo usar:

En el directorio `/home`, ejecutar:

`mkdir gestor_contrasenas`

`cd gestor_contrasenas`

`wget https://raw.githubusercontent.com/gonzalezalfie/gestor_contrasenas/main/gestor_contrasenas.py`

`chmod +x gestor_contrasenas.py`

`echo "python3 $HOME/gestor_contrasenas/gestor_contrasenas.py" > gestor_contrasenas`

`chmod +x gestor_contrasenas`

`sudo mv gestor_contrasenas /usr/bin`

Asegúrate de tener python 3.7> y las librerías 

* numpy
* pandas
* pycryptodome

Puedes instalar `miniconda` de la siguiente manera:

`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`

`chmod +x Miniconda3-latest-Linux-x86_64.sh`

`./Miniconda3-latest-Linux-x86_64.sh`

Dale Enter hasta que te pregunte yes/no. Dale yes.

Ejecuta 

`source ~/.bashrc`

Ejecuta `which pyhton`. Debería aparecer algo como esto:

`/home/ubuntu/miniconda3/bin/python`

Ejecuta 

`pip install --upgrade pip`

`pip install numpy`

`pip install pandas`

`pip install pycryptodome`

Escribe 

gestor_contrasenas
