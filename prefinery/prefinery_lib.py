import httplib2
from xml.dom.minidom import parseString
from django.conf import settings

_keys = ['PREFINERY_SUBDOMAIN', 'PREFINERY_KEY', 'PREFINERY_BETA_ID']
_missing_keys = [k for k in _keys if not hasattr(settings, k)]
if len(_missing_keys) >0:
    raise Exception("The following settings are missing: %s" % _missing_keys)

def beta_url(path, extra=''):
    url = 'https://'+settings.PREFINERY_SUBDOMAIN+'.prefinery.com/api/v1/betas/'+str(settings.PREFINERY_BETA_ID)
    url += path
    url += '?api_key='+settings.PREFINERY_KEY+'&'+extra
    return url  
    
def create_tester(email, status):
    xml = '<?xml version="1.0" encoding="UTF-8"?><tester><email>'+email+'</email><status>'+status+'</status></tester>'
    h = httplib2.Http()
    url = beta_url('/testers.xml')
    headers = {'Content-type': 'text/xml'}
    resp, content = h.request(url, 'POST', headers=headers, body=xml) 
    return resp

def delete_tester(id):
    h = httplib2.Http()
    url = beta_url('/testers/'+id+'.xml')
    resp, content = h.request(url, 'DELETE') 
    return resp

def get_tester_friend_invitations_remaining(tester_email):
    h = httplib2.Http()
    url = beta_url('/testers.xml', 'email='+tester_email)
    resp, content = h.request(url) 
    try:
        xml = parseString(content)
        count = xml.getElementsByTagName('friend-invitations-remaining')[0]
        for node in count.childNodes:
            if node.data:
                return node.data
    except Exception as e:
        return None

def get_tester_id_by_email(tester_email):
    h = httplib2.Http()
    url = beta_url('/testers.xml', 'email='+tester_email)
    resp, content = h.request(url) 
    try:
        xml = parseString(content)
        id = xml.getElementsByTagName('id')[0]
        for node in id.childNodes:
            if node.data:
                return node.data
    except Exception as e:
        return None

def get_tester_code(tester_id):
    h = httplib2.Http()
    url = beta_url('/testers/'+tester_id+'.xml')
    resp, content = h.request(url) 
    try:
        xml = parseString(content)
        id = xml.getElementsByTagName('invitation-code')[0]
        for node in id.childNodes:
            if node.data:
                if getattr(settings, "PREFINERY_USE_SHORT_CODES", False):
                    return node.data[:10]
                else:
                    return node.data
    except Exception as e:
        return None

def verify_code(tester_id, code):
    h = httplib2.Http()
    url = beta_url('/testers/'+tester_id+'/verify.xml', 'invitation_code='+code)
    resp, content = h.request(url)
    if resp.status == 200:
        return parseString(content)
    else:
        return None

def set_tester_status(tester_id, status):
    xml = '<?xml version="1.0" encoding="UTF-8"?><tester><status>'+status+'</status></tester>'
    h = httplib2.Http()
    url = beta_url('/testers/'+tester_id+'.xml')
    headers = {'Content-type': 'text/xml'}
    resp, content = h.request(url, 'PUT', headers=headers, body=xml) 
    if resp.status == 200:
        return True
    else:
        return False
