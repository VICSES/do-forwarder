import zeep
import hashlib
from config import didww_access_key, didww_account_name

# Example client to change didww redirect

h = hashlib.sha1()
h.update(didww_account_name.encode())
h.update(didww_access_key.encode())
auth_str = h.hexdigest()

# API Docs, both req. some miss detail in other
#  https://my.didww.com/api/api2_docs#update_mapping
#  http://open.didww.com/index.php/8._Update_Mapping
#  Also see wsdl.xml for undocumented functions

wsdl = "https://api.didww.com/api2/?wsdl"
client = zeep.Client(wsdl=wsdl)
#client.service.didww_getdidwwregions(auth_string=auth_str, country_iso='RU', city_prefix='', last_request_gmt='', city_id='')

#client.service.didww_getservicelist(auth_string=auth_str, customer_id='0')

def get_did_num(customer_id=0):
    dids = client.service.didww_getservicelist(auth_string=auth_str, customer_id=customer_id)

    # dids is a list of service_data dicts

    # Result
    #   0   Success
    #  -1   Errors
    # DID Status
    #  -2   Removed (moved to SAP, SRL, NRL, reserved by customer or will be removed soon)
    #  -1   Blocked (Expired, Canceled or Suspended)
    #   0   Unknown (DID number does not exist or status is unknown)
    #   1   Active DID number
    # Order Status
    #   Completed   Completed order
    #   Pending     Pending order
    #   Canceled    Order was canceled
    # Order Status -> DID Status possible values
    #   Completed  1
    #   Pending    -1, 0, 1
    #   Canceled   2, -1, 0

    good = filter(lambda x: x.result == 0 and x.order_status == 'Completed', dids)

    return next(good).did_number


customer_id = 0
did_number = get_did_num(customer_id)

target_num = '61439069336'
target_num = '61423123123'

# This creates a new voice trunk, named "PSTN Num"
# Every call, even identical, creates a new trunk
# Support request submitted querying if this was a problem

r = client.service.didww_updatemapping(
    auth_string = auth_str,
    customer_id = customer_id,
    did_number  = did_number,
    map_data    = {
        "map_type": "PSTN",
        "map_proto": 0,
        "map_detail": target_num, # International format
        "map_pref_server": 0, # Local server, automatic detection
        "map_itsp_id": None,
        "cli_format": "raw",
        "cli_prefix": "",
    }
)
print(r)
