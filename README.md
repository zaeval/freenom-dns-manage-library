# freenom-dns-manage-library
freedom-dns-manage-library ( domain register, record setting etc..)
this library version is beta. so now version supported only dns add record & modify & get dns list.

# How 2 Use

1. import fnml

2. first **call** fnml.__init__(your_ip, freenom_id, freenom_passwd, your_dns) **this function**
it works with login session!

> it must not required ip & dns but  freenom_id & freenom_passwd is must required.
https://my.freenom.com/clientarea.php << **signup here**

3. **then** fnml.dns_modify_or_add(ip_address, your_dns) **when**
 you want add record or modify **call this function**
