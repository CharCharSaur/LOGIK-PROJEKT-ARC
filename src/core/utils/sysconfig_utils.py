import json
import os
from functools import lru_cache

from src.core.utils import get_short_hostname


# Crude way to  get current Flame version and hostname to resolve config file correctly.
FLAME_VERSION = os.path.basename(os.path.realpath("/opt/Autodesk/cfg/.current")).lstrip(".")
HOSTNAME = get_short_hostname()

# matches their tokens in the sysconfig.cfg
TOKENS = {"<VERSION>": FLAME_VERSION, "<hostname>": HOSTNAME}

# takes a syscfg.cfg path and resolves the config the way Flame would. Allows shared cfgs.
# _seen is used to avoid circular loops
def resolve_sysconfig_path(path, _seen=frozenset()):
	# even though load_syscfg resolves tokens, path is a raw string so may not have been parsed
	path = path.replace("<VERSION>", FLAME_VERSION)
	real = os.path.realpath(path)

	# stops recursion loop
	if real in _seen:
		return real

	# loads config data and parses for TOKENS and handles errors.
	config_data = load_syscfg(real)
	if not config_data:
		return real

	versions_dict = config_data.get("configuration", {}).get("versions", {})
	new_syscfg_path = versions_dict.get(FLAME_VERSION) or versions_dict.get("<VERSION>")

	if not new_syscfg_path:
		return real

	if not os.path.exists(new_syscfg_path):
		return real

	return resolve_sysconfig_path(new_syscfg_path, _seen | {real})

# cached to avoid repeated io hits
@lru_cache
def load_syscfg(path):
	try:
		with open(path, 'r') as f:
			config_data = json.load(f)
		if config_data:
			config_data = substitute_tokens(config_data, TOKENS)
		return config_data
	# Generic errors copied from get_systemconfig_flame_*_dir.py scripts
	except FileNotFoundError:
		print(
			f"Error: sysconfig.cfg not found at:"
			f"{path}"
		)
		return None
	except json.JSONDecodeError:
		print(
			f"Error: Could not decode JSON from:"
			f"{path}"
		)
		return None
	except Exception as e:
		print(
			f"Error loading default Flame catalog directory:"
			f"{e}"
		)
		return None

# Loops through json structure and substitutes tokens
def substitute_tokens(data, tokens):
	if isinstance(data, dict):
		return {k: substitute_tokens(v, tokens) for k, v in data.items()}
	if isinstance(data, list):
		return [substitute_tokens(v, tokens) for v in data]
	if isinstance(data, str):
		for token, value in tokens.items():
			data = data.replace(token, value)
		return data
	return data
