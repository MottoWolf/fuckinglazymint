#!/bin/bash
#Script que llama y ejecuta el resto de scripts

echo "***********************************************"
echo "*    Elige de entre las siguiente opciones    *"
echo "*    1. Añadir usuario                        *"
echo "*    2. Cifrar disco                          *"
echo "*    6. Salir                                 *"
echo "***********************************************"

echo "Introduce un número"
read option

case $option in
        1) sh 1.sh
           rm ./1.sh
        ;;
        2) sh 2.sh
           rm ./2.sh
        ;;
        6) exit
        ;;
esac

sh ./metascript.sh
