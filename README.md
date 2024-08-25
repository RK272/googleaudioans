# Multilingual Assistant 


# How to run?
### STEPS:

Clone the repository

```bash
Project repo: https://github.com/
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n llmapp python=3.8 -y
```

```bash
conda activate llmapp
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```

### Create a `.env` file in the root directory and add your GOOGLE_API_KEY credentials as follows:

```ini
GOOGLE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# Finally run the following command
streamlit run app.py
```

Now,
```bash
open up localhost:
```


### Techstack Used:

- Python
- Google API
- Streamlit
- PaLM2
- s2t
- t2s
##How to Deploy Streamlit app on EC2 instance

1. Login with your AWS console and launch an EC2 instance or google cloud
2. Run the following commands

1 sudo apt update
2 sudo apt-get update
3 sudo apt upgrade -y
4 sudo apt install git curl unzip tar make sudo vim wget -y
5 git clone "Your-repository"
6 sudo apt install python3-pip
7 #Temporary running
8 python3 -m streamlit run app.py
9 #Permanent running
10 nohup python3 -m streamlit run app.py
11 #GCP PORT opening
12 gcloud compute firewall-rules create <policyname> --allow tcp:<port number> --source-ranges=0.0.0.0/0 --description="<your-description-here>"

tree 
if not execute 
sudo apt install tree


speech recogonizatio -- sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo pip install pyaudio

gcloud compute firewall-rules create apppol --allow tcp:8000 --source-ranges=0.0.0.0/0 --description="<your-description-here>"


