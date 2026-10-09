#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  ____  _____  _    _  ____  ____  ____  ____     ____  _  _     ___  _   _  __  __  ___   ___  _  _ 
# (  _ \(  _  )( \/\/ )( ___)(  _ \( ___)(  _ \   (  _ \( \/ )   / __)( )_( )/. |/  )(__ \ / _ \( \( )
#  )___/ )(_)(  )    (  )__)  )   / )__)  )(_) )   ) _ < \  /   ( (__  ) _ ((_  _))(  / _/( (_) ))  ( 
# (__)  (_____)(__/\__)(____)(_)\_)(____)(____/   (____/ (__)    \___)(_) (_) (_)(__)(____)\___/(_)\_)

from __future__ import annotations

import argparse
import os
import signal
import sys
from typing import Optional

import requests
from rich.console import Console

from core.apis import load_apis
from core.config import load_config, save_config
from ui.tui import TuiApp
from ui.screens.main_menu import MainMenuScreen
from ui.screens.start_screen import StartScreen
from ui.screens.settings_screen import SettingsScreen
from ui.screens.apis_screen import ApisScreen
from ui.screens.updater_screen import UpdaterScreen
from ui.screens.attack_screen import AttackScreen
from ui.screens.about_screen import AboutScreen
from ui.screens.help_screen import HelpScreen
from ui.screens.logs_screen import LogsScreen
from ui.screens.history_screen import HistoryScreen
from utils.logger import setup_logger
from utils.paths import CONFIG_PATH
from utils.version import APP_NAME, APP_VERSION

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)


def _register_screens(app: TuiApp) -> None:
    app.register(MainMenuScreen)
    app.register(StartScreen)
    app.register(SettingsScreen)
    app.register(ApisScreen)
    app.register(UpdaterScreen)
    app.register(AttackScreen)
    app.register(AboutScreen)
    app.register(HelpScreen)
    app.register(LogsScreen)
    app.register(HistoryScreen)


def run(config_path: Optional[str] = None) -> None:
    console = Console()
    cfg = load_config(config_path)
    try:
        apis = load_apis()
    except Exception as exc:
        console.print(f"[bold red]Failed to load apis.json:[/] {exc}")
        sys.exit(1)

    logger = setup_logger(cfg)
    tui = TuiApp(console, cfg, apis, logger)
    _register_screens(tui)
    tui.push("main_menu")

    signal.signal(signal.SIGINT, lambda *_: os.kill(os.getpid(), signal.SIGTERM))

    try:
        tui.run()
    finally:
        save_config(cfg, config_path)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=f"{APP_NAME} v{APP_VERSION} - SMS prank tool (educational).",
    )
    parser.add_argument(
        "--config", metavar="PATH",
        help=f"Path to config.json (default: {CONFIG_PATH})",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        run(config_path=args.config)
    except KeyboardInterrupt:
        print("\n[!] Interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()