











class ImportedModule():
	def __init__(s, ram):
		for k in ram:
			exec(f"s.{k}= ram[k]")


def imprt(dir):
	dir+=".py"
	f= open(dir,"rb")
	cont= f.read()
	f.close()

	compiled= compile(cont, dir, "exec")
	del cont
	ram= {}
	exec(compiled, ram)

	return ImportedModule(ram)
