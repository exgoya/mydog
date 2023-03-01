# mydog

python version : 3.9.16   
pip version : 23.0.1  

# mongodb intall
https://www.mongodb.com/docs/manual/administration/install-community/  

# install
git clone https://github.com/exgoya/mydog.git  
cd mydog  
python -m venv venv  
source venv/bin/activate  
python -m pip install --upgrade pip  
python -m pip install -r requirements.txt           

# config settings
vi secrets.json #naver_api 는 https://developers.naver.com/apps/#/register 사이트에서 신청해야 합니다.  
{  
"MONGO_DB_NAME":"Mydogdb",  
"MONGO_URL":"mongodb://localhost:27017/mydog?retryWrites=true&w=majority",  
"NAVER_API_ID":"naverapi_id",  
"NAVER_API_SECRET":"naverapi_secret"  
}    
  
