#!/bin/bash

sed -i -e "s/your_gmail/$1/g" ./ChatterBox_template.py ./ChatterBox.py
sed -i -e "s/your_gmail/$1/g" ./reset/Reset_Login_template.py ./reset/Reset_Login.py
sed -i -e "s/your_gmail/$1/g" ./reset/Reset_Simulator_template.py ./reset/Reset_Simulator.py

sed -i -e "s/your_password/$2/g" ./ChatterBox_template.py ./ChatterBox.py
sed -i -e "s/your_password/$2/g" ./reset/Reset_Login_template.py ./reset/Reset_Login.py
sed -i -e "s/your_password/$2/g" ./reset/Reset_Simulator_template.py ./reset/Reset_Simulator.py