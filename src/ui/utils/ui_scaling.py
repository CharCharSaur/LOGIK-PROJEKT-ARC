#Just some extra jank to get the UI to scale if below a certain factor. Some layout glitching, but could be worse.

import re

def scale_ui(ui_config, scaling_factor):
	if scaling_factor <=1:
		new_config = ui_config

		for attr_name in dir(new_config):
			if not attr_name.startswith("__"):
				value = getattr(new_config, attr_name)
				if isinstance(value, (int, float)):
					new_value = int(round(value * scaling_factor))
					setattr(new_config, attr_name, new_value)

				# Scale tuples of numbers (e.g. (0, 4, 0, 4))
				elif isinstance(value, tuple) and all(isinstance(v, (int, float)) for v in value):
					scaled_tuple = tuple(int(round(v * scaling_factor)) for v in value)
					setattr(new_config, attr_name, scaled_tuple)
		return new_config
	else:
		return ui_config

def get_scaling_factor(ui_config, screen_height):
	screen_height = 1080
	tolerance = screen_height * ui_config.TOLERANCE
	scaling_factor = screen_height / ui_config.WINDOW_HEIGHT * ui_config.TOLERANCE

	if ui_config.WINDOW_HEIGHT > tolerance:
		return scaling_factor
	else:
		return None

def scale_qss(qss: str, factor: float) -> str:
	# matches numbers followed by px or pt, but avoids touching rgb(…)/rgba(…)
	_UNIT_RE = re.compile(r'(?P<num>\d+(\.\d+)?)\s*(?P<unit>px|pt)\b')

	def repl(m):
		val = float(m.group('num')) * factor
		unit = m.group('unit')
		return f"{int(round(val))}{unit}"

	return _UNIT_RE.sub(repl, qss)