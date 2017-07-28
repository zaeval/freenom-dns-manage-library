import requests
import threading


def get_my_public_ip():
    ip_address = requests.get("http://ipecho.net/plain").text
    print(ip_address)
    return ip_address


old_ip_address = ''
username = ''
password = ''
manage_dns = ''
ses = requests.Session()


def modify_dns(ip_address=None, para_manage_dns=None):
    global old_ip_address
    print("old ip = " + old_ip_address)

    if ip_address == None:
        ip_address = get_my_public_ip()

    if para_manage_dns != None:
        manage_dns = para_manage_dns

    manage_dns_id = get_dns_id(manage_dns)

    if old_ip_address != ip_address:
        print("reload dns..." + ip_address)

        r = ses.post('https://my.freenom.com/clientarea.php?managedns=' + manage_dns + '&domainid=' + manage_dns_id,
                     verify=False)

        token = r.text[r.text.find('name="token"'):].split('"')[3]
        dnsaction = r.text[r.text.find('name="dnsaction"'):].split('"')[3]

        form_data = {
            "token": token,
            "dnsaction": dnsaction,
            "records[0][line]": "",
            "records[0][type]": "A",
            "records[0][name]": "",
            "records[0][ttl]": "300",
            "records[0][value]": ip_address,
            "records[1][line]": "",
            "records[1][type]": "A",
            "records[1][name]": "WWW",
            "records[1][ttl]": "300",
            "records[1][value]": ip_address
        }

        r = ses.post('https://my.freenom.com/clientarea.php?managedns=' + manage_dns + '&domainid=' + manage_dns_id,
                     verify=False,
                     data=form_data)
        old_ip_address = ip_address


def login():
    r = ses.post('https://my.freenom.com/dologin.php', verify=False, data={
        'username': username,
        'password': password
    })


def get_dns_id(para_manage_dns):
    manage_dns_id = ''
    return manage_dns_id


def get_dns_list():
    dns_list = {}
    return dns_list
