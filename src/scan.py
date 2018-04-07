import dynamixel


ports = dynamixel.get_available_ports()
if not ports :
	raise IOError("No ports found ")

print "Connecting to ",ports[0]

dxl = dynamixel.Dxl(ports[0])
ids = dxl.scan(25)

print ids