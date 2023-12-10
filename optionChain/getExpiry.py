import uuid
import calendar
from datetime import datetime, timedelta

class Expiry:
    dateFormat = "%Y-%m-%d"
    timeFormat = "%H:%M:%S"
    dateTimeFormat = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def monthly_expiry(instrument_type, exchange, numMonthsPlus):
        if((instrument_type == "stock_option" and exchange == "NSE" and numMonthsPlus != None) or
           (instrument_type == "index_option" and exchange == "NSE" and numMonthsPlus != None)):
            return True
        else:
            return False

    @staticmethod
    def weekly_expiry(instrument_type, exchange, numWeeksPlus):
        if(instrument_type == "index_option" and exchange == "NSE" and numWeeksPlus != None):
            return True
        else:
            return False

    @staticmethod
    def monthly_expiry_mx(instrument_type, exchange, expiry_type):
        if((instrument_type == "stock_option" and exchange == "NSE" and expiry_type == "monthly") or
           (instrument_type == "index_option" and exchange == "NSE" and expiry_type == "monthly")):
            return True
        else:
            return False

    @staticmethod
    def weekly_expiry_mx(instrument_type, exchange, expiry_type):
        if((instrument_type == "index_option" and exchange == "NSE" and expiry_type == "weekly")):
            return True
        else:
            return False

    @staticmethod
    def stepstrike(step, strike, strikemultiple):
        return strike+(step*strikemultiple)

    @staticmethod
    def tradeableStrike(strike, spot):
        if(strike > spot*1.3 or strike < spot*0.7):
            return False
        return True

    @staticmethod
    def getTodayDateStr():
        return Expiry.convertToDateStr(datetime.now())

    @staticmethod
    def convertToDateStr(datetimeObj):
        return datetimeObj.strftime(Expiry.dateFormat)

    @staticmethod
    def getNearestStrikePrice(price, base):
        return (base * round(price/base))

    @staticmethod
    def generateTradeID():
        # This is a string, not to be used for DB purposes,use just to fetch a single order status
        return str(uuid.uuid4())

    @staticmethod
    def getWeeklyExpiryDayDate(dateTimeObj=None):
        if dateTimeObj == None:
            dateTimeObj = datetime.now()
        daysToAdd = 0
        if dateTimeObj.weekday() >= 3:
            daysToAdd = -1 * (dateTimeObj.weekday() - 3)
        else:
            daysToAdd = 3 - dateTimeObj.weekday()
        datetimeExpiryDay = dateTimeObj + timedelta(days=daysToAdd)
        while Expiry.isHoliday(datetimeExpiryDay) == True:
            datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)

        datetimeExpiryDay = Expiry.getTimeOfDay(0, 0, 0, datetimeExpiryDay)
        return datetimeExpiryDay

    @staticmethod
    def getMonthlyExpiryDayDate(datetimeObj=None):
        if datetimeObj == None:
            datetimeObj = datetime.now()
        year = datetimeObj.year
        month = datetimeObj.month
        # 2nd entry is the last day of the month
        lastDay = calendar.monthrange(year, month)[1]
        datetimeExpiryDay = datetime(year, month, lastDay)
        while calendar.day_name[datetimeExpiryDay.weekday()] != 'Thursday':
            datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)
        while Expiry.isHoliday(datetimeExpiryDay) == True:
            datetimeExpiryDay = datetimeExpiryDay - timedelta(days=1)

        datetimeExpiryDay = Expiry.getTimeOfDay(0, 0, 0, datetimeExpiryDay)
        return datetimeExpiryDay

    @staticmethod
    def getMarketStartTime(dateTimeObj=None):
        return Expiry.getTimeOfDay(9, 15, 0, dateTimeObj)

    @staticmethod
    def getMarketEndTime(dateTimeObj=None):
        return Expiry.getTimeOfDay(15, 30, 0, dateTimeObj)

    @staticmethod
    def getTimeOfDay(hours, minutes, seconds, dateTimeObj=None):
        if dateTimeObj == None:
            dateTimeObj = datetime.now()
        dateTimeObj = dateTimeObj.replace(
            hour=hours, minute=minutes, second=seconds, microsecond=0)
        return dateTimeObj

    @staticmethod
    def getTimeOfToDay(hours, minutes, seconds):
        return Expiry.getTimeOfDay(hours, minutes, seconds, datetime.now())

    @staticmethod
    def isHoliday(datetimeObj):
        dayOfWeek = calendar.day_name[datetimeObj.weekday()]
        if dayOfWeek == 'Saturday' or dayOfWeek == 'Sunday':
            return True

        dateStr = Expiry.convertToDateStr(datetimeObj)
        #holidays = getHolidays()
        # if (dateStr in holidays):
        #  return True
        # else:
        return False

    @staticmethod
    def prepareOptionsSymbol(inputSymbol, strike, optionType, expiryDate):
        optionSymbol = inputSymbol + expiryDate + \
            str(strike) + optionType.upper()

        return optionSymbol

    @staticmethod
    def getMonthlyExpiryDate(numMonthsPlus=0):
        expiryDateTime = Expiry.getMonthlyExpiryDayDate()
        expiryDateMarketEndTime = Expiry.getMarketEndTime(expiryDateTime)
        if numMonthsPlus > 0:
            expiryDateTime = expiryDateTime + \
                timedelta(days=numMonthsPlus * 29)
            expiryDateTime = Expiry.getMonthlyExpiryDayDate(expiryDateTime)
        monthShort = calendar.month_name[expiryDateTime.month].upper()[0:3]
        year2Digits = str(expiryDateTime.year)[2:]

        return str(year2Digits) + monthShort

    @staticmethod
    def getWeeklyExpiryDate(numWeeksPlus=0):
        expiryDateTime = Expiry.getWeeklyExpiryDayDate()
        todayMarketStartTime = Expiry.getMarketStartTime()
        expiryDayMarketEndTime = Expiry.getMarketEndTime(expiryDateTime)
        if numWeeksPlus > 0:
            expiryDateTime = expiryDateTime + timedelta(days=numWeeksPlus * 7)
            expiryDateTime = Expiry.getWeeklyExpiryDayDate(expiryDateTime)
        if todayMarketStartTime > expiryDayMarketEndTime:
            expiryDateTime = expiryDateTime + timedelta(days=6)
            expiryDateTime = Expiry.getWeeklyExpiryDayDate(expiryDateTime)

        # Check if monthly and weekly expiry same
        year2Digits = str(expiryDateTime.year)[2:]

        # Changing for Shoonya
        d = expiryDateTime.day
        dStr = ("0" + str(d)) if d < 10 else str(d)
        monthShort = calendar.month_name[expiryDateTime.month].upper()[0:3]
        
        return dStr + monthShort + str(year2Digits)
    
if __name__=='__main__':
    expiry=Expiry()
    expiryDate=expiry.getWeeklyExpiryDate(numWeeksPlus=0)
    print(expiryDate)