from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset
from sys import argv, stderr, exit
#from timeout import timeout


def getmeta(tempfile):
  try:
    
    filename = tempfile
    filename, realname = unicodeFilename(filename), filename
    parser = createParser(filename, realname)
    if not parser:
      print >>stderr, "Unable to parse file"
      return "error"
    try:
      metadata = extractMetadata(parser)
    except HachoirError, err:
      print "Metadata extraction error: %s" % unicode(err)
      metadata = None
    if not metadata:
      print "Unable to extract metadata"
      return "error"

    text = metadata.exportPlaintext()
    charset = getTerminalCharset()
    return text
  except Exception:
    print "Exception In Processing\n"
    pass
  
  '''
  for line in text:
        
    print makePrintable(line, charset) 
  '''
