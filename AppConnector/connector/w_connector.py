def do_connect(item, objItem):
	if item[2] == objItem[2]:
		return False

	if item[1] == objItem[1]:
		return True

	return False