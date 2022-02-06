# ChatterBox

## Requirement
- System
    - OS: Linux
    - Actions on Google simulator using Dialogflow (not Actions Builder)
- Tool
    - Python3
    - In English
        - Stanford CoreNLP Server
        - NLTK
        - Stanza
    - In Japanese
        - JUMAN++ 2.0.0-rc3
        - KNP 4.20
        - pyknp

## Installation
```
git clone https://github.com/VAapp-system/ChatterBox.git
cd ChatterBox
./install.sh <Gmail Address> <Gmail Password> <Actions on Google Project Name>
```
- In English
```
./setNLP.sh <Stanford CoreNLP Server URL>
```
## Usage
```
./setup.sh <Language (EN/JA)>
python3 ChatterBox.py <Language (EN/JA)>
```
