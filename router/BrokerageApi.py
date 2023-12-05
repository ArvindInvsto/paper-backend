from fastapi import Form, status, APIRouter, Depends, Header, Request
from logics import BrokerageApi
from pydantic import BaseModel
router = APIRouter(tags=["Connect Brokerage"])

class editBrokerageSettings(BaseModel):
    user_id: int 
    brokerage_id: str
    brokerage_user_id: str = None
    vc: str = None
    api_key: str = None
    api_secret_key: str = None
    imei: str = None
    password: str = None
    factor2: str = None
#############     GET APIS      #############
@router.get("/getbrokerageoption", status_code=status.HTTP_200_OK)
async def get_brokerage_option():
    return BrokerageApi.get_brokerage_option()

@router.get("/getallbrokerages", status_code=status.HTTP_200_OK)
async def get_all_brokerage_list(userid: int = Header(None)):
    return BrokerageApi.get_all_brokerage_list(userid)

@router.get("/getactivebrokerages", status_code=status.HTTP_200_OK)
async def get_active_brokerage_list(userid: int = Header(None)):
    return BrokerageApi.get_active_brokerage_list(userid)

@router.get("/getbrokerageinfo", status_code=status.HTTP_200_OK)
async def get_brokerage_info(user_id: int = Header(None)):
    return BrokerageApi.get_brokerage_info(user_id)

@router.get("/get_brokerage_setting_id",status_code=status.HTTP_200_OK)
async def get_brokerage_setting_id(user_id:int = Header(None), brokerage_id: str = Header(None)):
    return BrokerageApi.get_brokerage_setting_id(user_id,brokerage_id)


#############     POST APIS      #############
# @router.post("/activatebrokerage", status_code=status.HTTP_200_OK)
# async def activate_brokerage(brokerage_setting_id: int = Header(None), otp: int = Header(None)):
#     return BrokerageApi.activate_brokerage(brokerage_setting_id)

@router.post("/activate-paper",status_code=status.HTTP_200_OK)
async def activate_paper(brokerage_setting_id : int  = Header()):
    return BrokerageApi.activate_paper(brokerage_setting_id)



# @router.post("/connectbrokerage", status_code=status.HTTP_200_OK)
# async def connect_brokerage(user_id: str = Header(None), brokerage_name: str = Header(None), brokerage_id: int = Header(None), brokerage_user_id: str = Header(None), vc: str = Header(None), factor2: str = Header(None), api_key: str = Header(None), api_secret_key: str = Header(None), imei: str = Header(None), brokerage_password: str = Header(None)):
#     return BrokerageApi.connect_brokerage(user_id, brokerage_user_id,brokerage_password, factor2, vc, api_key, api_secret_key, imei, brokerage_name, brokerage_id)

@router.post("/connect-paper", status_code=status.HTTP_200_OK)
async def connect_paper(user_id: str = Header(None), brokerage_id: str = Header(None)):
    return BrokerageApi.connect_paper(user_id, brokerage_id)




@router.post("/deactivatebrokerage", status_code=status.HTTP_200_OK)
async def deactivate_brokerage(brokerage_setting_id: int = Header(None)):
    return BrokerageApi.deactivate_brokerage(brokerage_setting_id)

@router.post("/removebrokerage", status_code=status.HTTP_200_OK)
async def remove_brokerage_setting(userid: int = Header(None), brokerage_setting_id: str = Header(None)):
    return BrokerageApi.remove_brokerage_setting(userid, brokerage_setting_id)

@router.post("/setbrokerage", status_code=status.HTTP_200_OK)
async def set_brokerage(strategy_id: int = Header(None), user_id: int = Header(None), brokerage_setting_id: int = Header(None)):
    return BrokerageApi.set_brokerage(strategy_id, user_id, brokerage_setting_id)

@router.put("/edit-brokerage", status_code=status.HTTP_200_OK)
async def edit_brokerage(item: editBrokerageSettings, brokerage_setting_id: int = Header(...)):
    return BrokerageApi.edit_brokerage(item, brokerage_setting_id)
# @router.get("/generatepapercredentials", status_code=status.HTTP_200_OK)
# async def generate_paper_credentials():
#     return BrokerageApi.generate_credentials()

# @router.post("/loginbrokerage", status_code=status.HTTP_200_OK)
# async def generate_paper_credentials():
#     return BrokerageApi.temp()