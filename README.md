# intermine-compose
Repo to handle docker orchestration in the cloud

## Mock API

### Step 0 (optional but recommended)
#### Create a python virtual environment
```bash
conda create -n intermine_compose python=3.6 && conda activate intermine_compose
```
### Step 1
#### Install connexion python package
```bash
pip install connexion[swagger-ui]
```
### Step 2
#### Create a mock server
```bash
connexion run openapi.json --mock=all -v --debug --stub
```
This will create a mock_api server in debug mode. It returns example responses defined in the openapi.json file.