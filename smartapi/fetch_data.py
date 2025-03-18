from logzero import logger
from login import login

def fetch_ltp(exchange, tradingsymbol, symboltoken):
    smart_api, auth_token, refresh_token = login()
    
    if smart_api:
        try:
            stock_params = {
                "exchange": exchange,
                "tradingsymbol": tradingsymbol,
                "symboltoken": symboltoken
            }
            ltp_data = smart_api.ltpData(**stock_params)
            logger.info(f"LTP Data: {ltp_data}")
            return ltp_data
        except Exception as e:
            logger.exception(f"Fetching LTP failed: {e}")

def fetch_historical_data(exchange, symboltoken, interval, fromdate, todate):
    smart_api, auth_token, refresh_token = login()
    
    if smart_api:
        try:
            historic_params = {
                "exchange": exchange,
                "symboltoken": symboltoken,
                "interval": interval,
                "fromdate": fromdate,
                "todate": todate
            }
            historical_data = smart_api.getCandleData(historic_params)
            logger.info(f"Historical Data: {historical_data}")
            return historical_data
        except Exception as e:
            logger.exception(f"Fetching historical data failed: {e}")
if __name__ == "__main__":
    ltp = fetch_ltp("NSE", "RELIANCE", "2885")
    print("📊 LTP Data:", ltp)
