from pydantic import BaseModel, validator

market_types = ['INDIA', 'US LARGECAP', 'US SMALLCAP', 'US MIDCAP']
markets = {'india': 'India', 'us largecap': 'US LargeCap', 'us smallcap': 'US SmallCap', 'us midcap': 'US MidCap'}


class basket(BaseModel):
    basket_name: str
    market_name: str
    instruments: str
    is_favorite: bool

    @validator('market_name')
    def c_match(cls, v):
        if v.upper() not in market_types:
            raise ValueError(f'market_name must be in {market_types}')
        return markets[v.lower()]

    @validator('basket_name')
    def b_match(cls, v):
        if len(v) < 1:
            raise ValueError("Basket name is not valid")
        return v
