#!/bin/bash

sed -i -e "s/your_gmail/$1/g" ./ChatterBox.py ./ChatterBox.py
sed -i -e "s/your_gmail/$1/g" ./reset/Reset_Login.py ./reset/Reset_Login.py
sed -i -e "s/your_gmail/$1/g" ./reset/Reset_Simulator.py ./reset/Reset_Simulator.py

sed -i -e "s/your_password/$2/g" ./ChatterBox.py ./ChatterBox.py
sed -i -e "s/your_password/$2/g" ./reset/Reset_Login.py ./reset/Reset_Login.py
sed -i -e "s/your_password/$2/g" ./reset/Reset_Simulator.py ./reset/Reset_Simulator.py