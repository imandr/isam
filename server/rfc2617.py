import re, hashlib, base64, time

def digest_client(url, username, password):
    from requests.auth import HTTPDigestAuth
    response = requests.get(url, auth=HTTPDigestAuth(username, password))
    return response.status_code, response.content

HashAlgorithm = "SHA-256"
HashAlgorithm_hashlib_name= "sha256"

def digest_server(realm, env, get_password):
    #
    # Server side authentication function
    # env is WSGI evironment
    # get_password is a function: password = get_password(realm, username)
    # 

    def checksum(data):
        m = hashlib.new(HashAlgorithm_hashlib_name)
        if isinstance(data, str):
            data = data.encode("utf-8")
        m.update(data)
        return m.hexdigest()

    auth_header = env.get("HTTP_AUTHORIZATION","")
    #print "auth_header:", auth_header
    matches = re.compile('Digest \s+ (.*)', re.I + re.X).match(auth_header)

    if not matches:
        # need "Authorization" header
        nonce = base64.b64encode(str(int(time.time())).encode("utf-8"))
        header = 'Digest realm="%s", nonce="%s", algorithm=%s, qop="auth"' % (realm, nonce, HashAlgorithm)
        return False, header        
    
    
    vals = re.compile(', \s*', re.I + re.X).split(matches.group(1))

    dict = {}

    pat = re.compile('(\S+?) \s* = \s* ("?) (.*) \\2', re.X)
    for val in vals:
        ms = pat.match(val)
        if ms:
            dict[ms.group(1)] = ms.group(3)

    user = dict['username']
    cfg_password = get_password(realm, user)
    if cfg_password == None:
        # unknown user
        return False, None

    a1 = checksum('%s:%s:%s' % (user, realm, cfg_password))        
    a2 = checksum('%s:%s' % (env['REQUEST_METHOD'], dict["uri"]))
    myresp = checksum('%s:%s:%s:%s:%s:%s' % (a1, dict['nonce'], dict['nc'], dict['cnonce'], dict['qop'], a2))
    if myresp == dict['response']:
        # success
        return True, user
    else:
        # password did not match
	    #print "signature mismatch"
        return False, None
