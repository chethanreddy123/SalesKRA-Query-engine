from fastapi import FastAPI, HTTPException, Request, Response
import google.generativeai as palm
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from pymongo.mongo_client import MongoClient
from loguru import logger
import random

palm.configure(api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM')
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
response = palm.chat(messages=["Jon is very good boy and works and microsoft"])
MongoDB_Key = "mongodb://aioverflow:12345@ac-pu6wews-shard-00-00.me4dkct.mongodb.net:27017,ac-pu6wews-shard-00-01.me4dkct.mongodb.net:27017,ac-pu6wews-shard-00-02.me4dkct.mongodb.net:27017/?ssl=true&replicaSet=atlas-jcoztp-shard-0&authSource=admin&retryWrites=true&w=majority"
Data = MongoClient(MongoDB_Key)
EmployeeData = Data['FinalAxisBankHackathon']['EmployeeData']
KRAsData = Data['FinalAxisBankHackathon']['KRAsData']



############### Additional Functions #####################

def generate_random_id():
    # Generate a random 6-digit number
    random_number = random.randint(100000, 999999)
    
    # Combine with the fixed string 'AXIS'
    new_id = f'AXIS{random_number}'
    
    return new_id

def generate_random_id_KRA():
    # Generate a random 6-digit number
    random_number = random.randint(100000, 999999)
    
    # Combine with the fixed string 'AXIS'
    new_id = f'KRA{random_number}'
    
    return new_id

############### API Endpoints #####################

@app.post("/chat/")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")
    
    if message is None:
        raise HTTPException(status_code=400, detail="Message not provided")

    global response
    if message.upper() == "Q":
        return {"response": "Goodbye!"}

    response = response.reply(message)
    return {"response": response.last}

@app.post("/AddEmployee/")
def NewPatient(info : dict):
    req_info = info
    req_info = dict(req_info)
    print(req_info)
    logger.info("recieved new patient details")
    req_info['personalInformation']['EmployeeID'] = generate_random_id()

    try:
        Check = EmployeeData.insert_one(req_info)
        if Check.acknowledged == True:
            logger.info("patient added successfully")
            return {"status": "success" , "EmployeeID": req_info['personalInformation']['EmployeeID']}
        else:
            logger.info("patient not added")
            return {"status": "failed"}
    except Exception as e:
        logger.error(e)
        return {"status": "failed"}
    
@app.post("/GetEmployee/")
def GetEmployee(info : dict):
    req_info = info
    req_info = dict(req_info)
    EmployeeID = req_info['EmployeeID']
    Result = EmployeeData.find_one({"personalInformation.EmployeeID": EmployeeID})
    if Result is None:
        return {"status": "failed"}
    else:
        del Result['_id']
        return Result

@app.get("/GetAllEmployees/")
def GetAllEmployees():
    logger.info("recieved all employee details")
    Result = list(EmployeeData.find({}))
    if Result is None:
        return {"status": "failed"}
    else:
        for i in Result:
            del i['_id']
        return Result


@app.post("/AddKRA/")
def AddKRA(info : dict):
    req_info = info
    req_info = dict(req_info)
    print(req_info)
    logger.info("recieved new patient details")
    req_info['KRAID'] = generate_random_id_KRA()
    try:
        Check = KRAsData.insert_one(req_info)
        if Check.acknowledged == True:
            logger.info("patient added successfully")
            return {"status": "success" , "KRAID": req_info['KRAID']}
        else:
            logger.info("patient not added")
            return {"status": "failed"}
    except Exception as e:
        logger.error(e)
        return {"status": "failed"}
    

@app.post("/GetKRA/")
def GetKRA(info : dict):
    req_info = info
    req_info = dict(req_info)
    KRA_ID = req_info['KRAID']
    Result = KRAsData.find_one({"KRAID": KRA_ID})
    if Result is None:
        return {"status": "failed"}
    else:
        del Result['_id']
        return Result