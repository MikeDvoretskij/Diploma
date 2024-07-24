import pubchempy as pcp
from joblib import Parallel, delayed
import json
import time
import requests
from tqdm import tqdm
import pandas as pd
import os

start_index = 1
max_index = 500_000 #69_265_710

def parsing(id):
    try:
        information_dict = json.loads(requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+str(id)+"/description/json").text)
        time.sleep(0.5)

        try:
            description = information_dict['InformationList']['Information'][1]["Description"]
            compaund = pcp.Compound.from_cid(id)
            smiles_unique = compaund.isomeric_smiles

            return {'id': id, 'smiles': smiles_unique, 'description': description}

        except Exception as ex:
            compaund = pcp.Compound.from_cid(id)
            smiles_unique = compaund.isomeric_smiles

            return {'id': id, 'smiles': smiles_unique, 'description': None}

    except Exception as ex:
        print(ex)

    return {'id': id, 'smiles': None, 'description': None}

data = Parallel(n_jobs=-1)(delayed(parsing)(id) for id in tqdm([i for i in range(start_index, max_index)]))

data = pd.DataFrame(data=data)

data.to_csv("./data/data.csv", index=False, mode='a')