#!/bin/bash

sed -e "s/nlp_url/$1/g" ./module/questionEN_template.py > ./module/questionEN.py