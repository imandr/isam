from kbstorage import KBCachedStorage

if __name__ == "__main__":
    import getopt, sys
    
    Usage = """
    python storage.py <root> get <key>
                      <root> put <key> <file>
                      <root> ls
    """
    
    opts, args = getopt.getopt(sys.argv[1:], "")
    if not args:
        print(Usage)
        sys.exit(2)
        
    root, command, args = args[0], args[1], args[2:]
    storage = KBCachedStorage(root)
    
    if command == "get":
        key = args[0]
        blob = storage[key]
        sys.stdout.write(blob.decode("utf-8"))
    
    elif command == "put":
        key, path = args
        blob = open(path, "rb").read()
        storage[key] = blob
        
    elif command == "ls":
        for k in storage.keys():
            meta = storage.meta(k)
            if isinstance(k, bytes):
                k = k.decode("utf-8")
            print("%-40s %d" % (k, meta["size"]))