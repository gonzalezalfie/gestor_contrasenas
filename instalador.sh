#!/bin/bash

mkdir $HOME/gestor_contrasenas

cd $HOME/gestor_contrasenas

wget https://raw.githubusercontent.com/gonzalezalfie/gestor_contrasenas/main/gestor_contrasenas.py

sudo chmod +x gestor_contrasenas.py

#sudo apt-get install python3-pip

#export LC_ALL=C

sudo apt-get install python3-numpy

sudo apt-get install python3-pandas

sudo apt-get install python3-crypto

sudo echo "python3 $HOME/gestor_contrasenas/gestor_contrasenas.py" > /usr/bin/gestor_contrasenas

sudo chmod +x /usr/bin/gestor_contrasenas

#echo "alias gestor_contrasenas='python3 $HOME/gestor_contrasenas/#gestor_contrasenas.py'" >> ~/.bashrc


