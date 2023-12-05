from database import BrokerageApi
from fastapi import FastAPI, Header, status, HTTPException, APIRouter

def get_brokerage_option():
    """
    Retrieves the available brokerage options
    """
    return BrokerageApi.get_brokerage_option()

def get_all_brokerage_list(user_id: int):
    """
    Retrieves a list of all brokerages
    """
    missing_headers = []
    if user_id is None:
        missing_headers.append("userid")
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    bro_list = BrokerageApi.get_all_brokerage_list(user_id)
    if bro_list:
        return bro_list
    return {"message":"User not connected to any brokerage."}

def get_active_brokerage_list(user_id: int):
    """
    Retrieves a list of active brokerages
    """
    missing_headers = []

    if user_id is None:
        missing_headers.append("userid")
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    
    bro_list = BrokerageApi.get_active_brokerage_list(user_id)
    if bro_list:
        return bro_list
    return {"message":"No active brokerage associated with the user."}

def get_brokerage_setting_id(user_id: int,brokerage_id:str):
    """
    Retrieves brokerage_setting_id based on user_id and brokerage_id
    """
    missing_headers = []
    if user_id is None:
        missing_headers.append("userid")
    if brokerage_id is None:
        missing_headers.append("brokerageid")
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    
    bro_list = BrokerageApi.get_brokerage_setting_id(user_id,brokerage_id)
    if bro_list:
        return bro_list
    return {"message":"No active brokerage associated with the user."}

# def connect_brokerage(user_id: str, brokerage_user_id: str, password: str, factor2: str, vc: str, api_key: str, api_secret_key: str, imei: str, brokerage: str, brokerage_id: int):
#     """
#     Save brokerage credentials
#     """
#     missing_headers = []
#     if user_id is None:
#         missing_headers.append("userid")
#     if brokerage_user_id is None:
#         missing_headers.append("brokerage_user_id")
#     if password is None:
#         missing_headers.append("password")
#     if factor2 is None:
#         missing_headers.append("factor2")
#     if vc is None:
#         missing_headers.append("vc")
#     if api_key is None:
#         missing_headers.append("api_key")
#     if imei is None:
#         missing_headers.append("imei")
#     if brokerage is None:
#         missing_headers.append("brokerage")
#     if brokerage_id is None:
#         missing_headers.append("brokerage_id")
#     if missing_headers:
#         raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    
#     return BrokerageApi.connect_brokerage(user_id, brokerage_user_id, password, factor2, vc, api_key, api_secret_key, imei, brokerage, brokerage_id)

def connect_paper(user_id: str, brokerage_id: str):
    """
    Save brokerage credentials
    """
    print(user_id,brokerage_id)
    missing_headers = []
    if user_id is None:
        missing_headers.append("userid")
    if brokerage_id is None:
        missing_headers.append("brokerage_id")
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    
    return BrokerageApi.connect_paper(user_id, brokerage_id)

def connect_finvasia(user_id: str, brokerage_user_id: str, password: str,  vc: str,  api_secret_key: str, imei: str,  brokerage_id: int):
    """
    Save brokerage credentials
    """
    missing_headers = []
    if user_id is None:
        missing_headers.append("userid")
    if brokerage_user_id is None:
        missing_headers.append("brokerage_user_id")
    if password is None:
        missing_headers.append("password")
    if vc is None:
        missing_headers.append("vc")
    if imei is None:
        missing_headers.append("imei")
    if brokerage_id is None:
        missing_headers.append("brokerage_id")
    if brokerage_user_id is None:
        missing_headers.append("brokerage_user_id")
    
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    
    return BrokerageApi.connect_finvasia(user_id, brokerage_user_id, password,  vc,  api_secret_key, imei,  brokerage_id)

def connect_dhan(user_id: str, brokerage_user_id: str,  brokerage_id: int):
    """
    Save brokerage credentials
    """
    missing_headers = []
    if user_id is None:
        missing_headers.append("userid")
    if brokerage_user_id is None:
        missing_headers.append("brokerage_user_id")
    if brokerage_id is None:
        missing_headers.append("brokerage_id")
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    
    return BrokerageApi.connect_dhan(user_id, brokerage_user_id,brokerage_id)

def activate_brokerage(brokerage_setting_id: int):
    """
    Activates a brokerage
    """
    if brokerage_setting_id is None:
        raise HTTPException(status_code=400, detail=f"Following values are missing: brokerage_setting_id")

    user = BrokerageApi.get_brokerage_user(brokerage_setting_id)
    user_subscription = BrokerageApi.get_subsctiber_user(brokerage_setting_id)
    if user is None:
        # details = BrokerageApi.get_user_details(userid, brokerage)
        # print(details)
        return {"message" : "Couldn't find the brokerage associated witht the user."}
        # return BrokerageApi.activate_brokerage(details["brokerage_setting_id"], details["brokerage"], details["user_id"], details["password"], details["factor2"], details["vc"], details["api_key"], details["api_secret_key"], details["imei"], details["brokerage_user_id"])
    elif user["is_active"]:
        return {"message" : "Brokerage is already active."}
    
    BrokerageApi.activate_brokerage(brokerage_setting_id)
    
    if user_subscription is not None and not user_subscription["brokerage_is_active"]:
        BrokerageApi.activate_brokerage_subscriber(brokerage_setting_id)
    return {"message" : "Brokerage is activated."}

def activate_paper(brokerage_setting_id: int):
    """
    Activates paper brokerage
    """
    if brokerage_setting_id is None:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {brokerage_setting_id}")

    user = BrokerageApi.get_brokerage_user(brokerage_setting_id)
    user_subscription = BrokerageApi.get_subsctiber_user(brokerage_setting_id)
    if user is None:
        return {"message" : "Couldn't find the brokerage associated witht the user."}
    elif user["is_active"]:
        return {"message" : "Brokerage is already active."}
    
    BrokerageApi.activate_paper(brokerage_setting_id)
    
    if user_subscription is not None and not user_subscription["brokerage_is_active"]:
        BrokerageApi.activate_brokerage_subscriber(brokerage_setting_id)
    return {"message" : "Brokerage is activated."}


def activate_finvasia(brokerage_setting_id: int, access_token : str , factor2 : str):
    """
    Activates finvasia brokerage
    """
    if access_token is None and factor2 is None:
        raise HTTPException(status_code=400, detail=f"Provide one of access_token or factor2")

    user = BrokerageApi.get_brokerage_user(brokerage_setting_id)
    user_subscription = BrokerageApi.get_subsctiber_user(brokerage_setting_id)
    if user is None:
        return {"message" : "Couldn't find the brokerage associated witht the user."}
    elif user["is_active"]:
        return {"message" : "Brokerage is already active."}
    
    BrokerageApi.activate_finvasia(brokerage_setting_id,access_token,factor2)
    
    if user_subscription is not None and not user_subscription["brokerage_is_active"]:
        BrokerageApi.activate_brokerage_subscriber(brokerage_setting_id)
    return {"message" : "Brokerage is activated."}
        

def deactivate_brokerage(brokerage_setting_id: int):
    """
    Deactivates a brokerage
    """
    # user = BrokerageApi.is_user_present(userid)
    if brokerage_setting_id is None:
        raise HTTPException(status_code=400, detail=f"Following values are missing: brokerage_setting_id")

    user = BrokerageApi.get_brokerage_user(brokerage_setting_id)
    strat_user = BrokerageApi.get_subsctiber_user(brokerage_setting_id)
    if user is None:
        return {"message": "Brokerage does not exists."}
    elif user and strat_user:
        return BrokerageApi.deactivate_brokerage_and_strategy(brokerage_setting_id)
    else:
        return BrokerageApi.deactivate_brokerage(brokerage_setting_id)


def get_brokerage_info(user_id: int):
    """
    Retrieves information about a brokerage associated with a user
    """
    if user_id is None:
        raise HTTPException(status_code=400, detail=f"Following values are missing: user_id")

    return BrokerageApi.get_brokerage_info(user_id)


def remove_brokerage_setting(user_id:int, brokerage_setting_id: str):
    """
    Removes a brokerage setting associated with a user
    """
    missing_headers = []
    if user_id is None:
        missing_headers.append("userid")
    if brokerage_setting_id is None:
        missing_headers.append("brokerage_setting_id")
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    
    user = BrokerageApi.get_brokerage_user(brokerage_setting_id)
    print(user)
    if user is None:
        return {"message" : "Couldn't find the brokerage associated with the user."}
    user = BrokerageApi.remove_stratsub_brokerage_setting(user_id, brokerage_setting_id)
    return BrokerageApi.remove_brokerage_setting(user_id, brokerage_setting_id)

def set_brokerage(strategy_id: int, user_id: int, brokerage_setting_id: int):
    """
    Merges data from three tables into a single table associated with a user.

        table1: strategy table.
        table2: strategy_settings.
        table3: brokerage_setting table.
        
    Returns:
        Inserts data into strategy_subscriber table that merges the data from all three tables.
    """
    missing_headers = []
    if strategy_id is None:
        missing_headers.append("strategy_id")
    if user_id is None:
        missing_headers.append("user_id")
    if brokerage_setting_id is None:
        missing_headers.append("brokerage_setting_id")
    if missing_headers:
        raise HTTPException(status_code=400, detail=f"Following values are missing: {', '.join(missing_headers)}")
    strategy_setting = BrokerageApi.get_strategy_setting_id(strategy_id)
    if strategy_setting:
        strategy_setting_id = strategy_setting["id"]
    else:
        raise HTTPException(status_code=400, detail="Strategy settings not found.")
    
    details=BrokerageApi.get_details(strategy_id, brokerage_setting_id, strategy_setting_id)
    return BrokerageApi.set_brokerage(brokerage_setting_id, details["brokerage_id"], user_id, details["password"], details["factor2"], details["vc"], details["api_key"], details["api_secret_key"], details["imei"], details["brokerage_user_id"], strategy_id, strategy_setting_id, details["brokerage_is_active"])


def edit_brokerage(editBrokerageSettings,brokerage_setting_id):
    """
    Edit brokerage settings for a specific user and brokerage type.
    """
    
    user_id = editBrokerageSettings.user_id
    brokerage_id = editBrokerageSettings.brokerage_id
    brokerage_user_id = editBrokerageSettings.brokerage_user_id
    password = editBrokerageSettings.password
    factor2  = editBrokerageSettings.factor2
    vc = editBrokerageSettings.vc
    api_key = editBrokerageSettings.api_key
    api_secret_key = editBrokerageSettings.api_secret_key
    imei = editBrokerageSettings.imei


    result = BrokerageApi.edit_brokerage(
        brokerage_setting_id, user_id, brokerage_user_id, password, factor2, vc, api_key, api_secret_key, imei, brokerage_id
    )

    return result