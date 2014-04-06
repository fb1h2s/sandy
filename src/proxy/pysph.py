from pysphere import VIServer

def revert(datastore):
  #vmsphear username and password
  server = VIServer()
  server.connect("101.91.1.21", "root", "Vsphear_root_password")

  vm1 = server.get_vm_by_path(datastore)
  print "Cuurrent Status",vm1.get_status()
  print "Reverting VM:", datastore 
  vm1.revert_to_snapshot()
  print "Vm reverted"


revert("[datastore1] WindowsXPRahul/WindowsXPRahul.vmx")