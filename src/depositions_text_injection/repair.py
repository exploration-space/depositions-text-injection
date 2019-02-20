import re

def repair_ids(text: str) -> str:
	text = re.sub('<([a-zA-Z_][A-Za-z-_.]*?) ([^<^>]?xml:id=")([0-9].*?")', "<\g<1> \g<2>\g<1>\g<3>", text) #  replace id's in tags with explixit xml:id value, if it starts with digit
	text = re.sub('(<text.*?)#id([0-9].*?")', "\g<1>#p\g<2>", text) #  replace id's in text @corresp tags, if it starts with digit
	return text
