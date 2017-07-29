import requests
import threading


def get_my_public_ip():
    ip_address = requests.get("http://ipecho.net/plain").text
    return ip_address


old_ip_address = ''
username = ''
password = ''
manage_dns = ''
ses = requests.Session()
request = None


# TODO: dns add or modify
def dns_modify_or_add(ip_address=None, para_manage_dns=None):
    global old_ip_address
    global manage_dns
    global ses
    global request

    print("old ip = " + old_ip_address)

    if ip_address == None:
        ip_address = get_my_public_ip()

    if para_manage_dns != None:
        manage_dns = para_manage_dns

    manage_dns_id = get_dns_id(manage_dns)

    if old_ip_address != ip_address:
        print("reload dns..." + ip_address)

        request = ses.post(
            'https://my.freenom.com/clientarea.php?managedns=' + manage_dns.split("http://")[1].rstrip('/') + '&domainid=' + manage_dns_id,
            verify=False)
        token = request.text[request.text.find('name="token"'):].split('"')[3]
        dnsaction = request.text[request.text.find('name="dnsaction"'):].split('"')[3]
        if dnsaction == 'add':
            field = "addrecord"
        elif dnsaction == 'modify':
            field = "records"

        form_data = {
            "token": token,
            "dnsaction": dnsaction,
            field+"[0][line]": "",
            field+"[0][type]": "A",
            field+"[0][name]": "",
            field+"[0][ttl]": "300",
            field+"[0][value]": ip_address,
            field+"[1][line]": "",
            field+"[1][type]": "A",
            field+"[1][name]": "WWW",
            field+"[1][ttl]": "300",
            field+"[1][value]": ip_address
        }

        request = ses.post(
            'https://my.freenom.com/clientarea.php?managedns=' + manage_dns.split("http://")[1].rstrip('/') + '&domainid=' + manage_dns_id,
            verify=False,
            data=form_data)
        old_ip_address = ip_address


# TODO: login
def login(para_username=None, para_password=None):
    global username
    global password
    global ses
    global request

    username = para_username
    password = para_password

    request = ses.post('https://my.freenom.com/dologin.php', verify=False, data={
        'username': username,
        'password': password
    })


# TODO: get dns id function
def get_dns_id(para_manage_dns):
    global ses
    manage_dns_id = get_dns_list().get(para_manage_dns, None)
    return manage_dns_id


# TODO: get dns list with dns_id function
def get_dns_list():
    global ses
    global request
    dns_list = {}

    request = ses.post('https://my.freenom.com/clientarea.php?action=domains', verify=False)

    domain = ''
    id = ''
    for obj in request.text.split('<td class="second">')[1:]:
        domain = obj[obj.index('http'):obj.index('" target')]
        id = obj.split('action=domaindetails&id=')[1]
        id = id[:id.index('">')]
        #print(domain + " "+id)
        dns_list[domain] = id
    return dns_list


def __init__(para_old_ip_address=None, para_username=None, para_password=None, para_manage_dns=None):
    global old_ip_address
    global username
    global password
    global manage_dns
    old_ip_address = para_old_ip_address
    username = para_username
    password = para_password
    manage_dns = para_manage_dns
    login(username,password)


