import os, time
import datetime
(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat("index.html")
print("last modified: %s" % datetime.datetime.fromtimestamp(mtime))
