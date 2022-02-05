#!/bin/bash

sed -e "s/your_gmail/$1/g" -e "s/your_password/$2/g" ./ChatterBox_template.py > ./ChatterBox.py
sed -e "s/your_gmail/$1/g" -e "s/your_password/$2/g" ./reset/Reset_Login_template.py > ./reset/Reset_Login.py
sed -e "s/your_gmail/$1/g" -e "s/your_password/$2/g" -e "s/your_project_name/$3/g" ./reset/Reset_Simulator_template.py > ./reset/Reset_Simulator.py
sed -e "s/your_project_name/$3/g" ./module/simulator_template.py > ./module/simulator.py
sed -e "s/nlp_url/$4/g" ./module/questionEN_template.py > ./module/questionEN.py