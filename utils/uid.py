import hashlib


def get_uid(thestr):
   thestr = thestr.encode('utf-8')
   md5 = hashlib.new("md5", thestr).hexdigest()
   first_half_bytes = md5[:16]
   last_half_bytes = md5[16:]
   first_half_int = int(first_half_bytes, 16)
   last_half_int = int(last_half_bytes, 16)
   xor_int = first_half_int ^ last_half_int
   uid = "%x" % xor_int
   return uid

