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
Before using ChatterBox, you need a metadata file (named page_info_(en/ja).json). Please use the metadata crawler.
```
cd metadata_crawler
python3 GetAppPageUrl.py <Language (EN/JA)>
python3 GetMetadata.py <Language (EN/JA)>

```
How to use ChatterBox.
```
./setup.sh <Language (EN/JA)>
python3 ChatterBox.py <Language (EN/JA)>
```

## Collectable Data
- JSON payload sent by VA apps
    - It contains the VA app response, Rich Response and Interactive Canvas configuration information, and Suggestions.
- Tree structure
- Data stored in User Storage
- Interactive Canvas HTML
- Analysis data by Background Checker
    - User Tracking
    - User Storage
    - User ID
    - URL
    - Interactive Canvas