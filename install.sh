#!/bin/bash

sed -e "s/your_gmail/$1/g" -e "s/your_password/$2/g" ./ChatterBox_template.py > ./ChatterBox.py
sed -e "s/your_gmail/$1/g" -e "s/your_password/$2/g" ./reset/Reset_Login_template.py > ./reset/Reset_Login.py
sed -e "s/your_gmail/$1/g" -e "s/your_password/$2/g" ./reset/Reset_Simulator_template.py > ./reset/Reset_Simulator.py