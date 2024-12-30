import datetime
import json
import logging
import os
import sys
from decimal import Decimal
from importlib import import_module
from pathlib import Path
from werkzeug.utils import secure_filename
import api.system.opt_locking.opt_locking as opt_locking
import database.models as models
from database.models import *
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import DeclareRule, Rule, LogicBank
from security.system.authorization import Grant, Security
from colorama import Fore, Style, init
import safrs
import subprocess


app_logger = logging.getLogger(__name__)
declare_logic_message = "ALERT:  *** No Rules Yet ***"  # printed in api_logic_server.py

rule_import_template = """
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
{rule_code}
"""

def set_rule_status(rule_id, status):
    subprocess.run([
            "python", "/opt/webgenai/database/manager.py", 
            "-R", rule_id,
            "--rule-status", status],
            cwd="/opt/webgenai")


def set_rule_error(rule_id, error):
    subprocess.run([
                "python", "/opt/webgenai/database/manager.py", 
                "-R", rule_id,
                "--rule-error", error],
                cwd="/opt/webgenai")


def load_exported_rules():
    """
    Load rules from export.json and activate them
    (we can't use eval, because logicbank uses inspect)
    
    write the rule code to a temporary file and import it as a module
    """
    export_file = Path('./docs/export/export.json')
    if not export_file.exists():
        app_logger.info(f"{export_file.resolve()} does not exist")
        return

    rule_code_dir = Path('./logic/wg_rules') # in the project root
    rule_code_dir.mkdir(parents=True, exist_ok=True)
    sys.path.append(f"{rule_code_dir}")
    
    try:    
        with open(export_file) as f:
            export = json.load(f)
        rules = export.get('rules', [])
    except Exception as exc:
        app_logger.warning(f"Failed to load rules from {export_file}: {exc}")
        return
    
    active_modules = []
    for rule in rules:
        app_logger.info(f"\n{Fore.BLUE}Loading rule {rule['name']} - {rule['id']}{Fore.GREEN}")
        rule_file = rule_code_dir / f"{secure_filename(rule['name'])}.py"
        try:
            with open(rule_file, 'w') as temp_file:
                rule_code = "\n".join([f"  {code}" for code in rule['code'].split("\n")])
                temp_file.write(rule_import_template.format(rule_code=rule_code))
                temp_file_path = temp_file.name
            module_name = Path(temp_file_path).stem
            rule_module = import_module(module_name)
            rule_module.init_rule()
            LogicBank.activate(session=safrs.DB.session, activator=rule_module.init_rule)
            if rule['status'] != "active":
                set_rule_status(rule['id'], "active")
            active_modules.append(module_name)
        except Exception as exc:
            app_logger.warning(f"{Fore.RED}Failed to activate rule code\n{rule['code']}\n{Fore.YELLOW}{type(exc).__name__}: {exc}\n")
            set_rule_error(rule['id'], f"{type(exc).__name__}: {exc}")
        
    for module_name in active_modules:
        rule_module = import_module(module_name)
        rule_module.init_rule()

    app_logger.info(f"{Style.RESET_ALL}Loaded Exported Rules")

def declare_logic():
    ''' Declarative multi-table derivations and constraints, extensible with Python.
 
    Brief background: see readme_declare_logic.md
    
    Your Code Goes Here - Use code completion (Rule.) to declare rules
    '''
    app_logger.error("Starting declare_logic.py! \n")
    
    try:
        load_exported_rules()
    except Exception as exc:
        app_logger.warning(f"Failed to load exported rules: {exc}")
        
    from logic.logic_discovery.auto_discovery import discover_logic
    discover_logic()

    # Logic from GenAI: (or, use your IDE w/ code completion)


    # End Logic from GenAI


    def handle_all(logic_row: LogicRow):  # #als: TIME / DATE STAMPING, OPTIMISTIC LOCKING
        """
        This is generic - executed for all classes.

        Invokes optimistic locking, and checks Grant permissions.

        Also provides user/date stamping.

        Args:
            logic_row (LogicRow): from LogicBank - old/new row, state
        """
        if logic_row.is_updated() and logic_row.old_row is not None and logic_row.nest_level == 0:
            opt_locking.opt_lock_patch(logic_row=logic_row)

        Grant.process_updates(logic_row=logic_row)

    Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all)

    #als rules report
    from api.system import api_utils
    # api_utils.rules_report()

    app_logger.debug("..logic/declare_logic.py (logic == rules + code)")

