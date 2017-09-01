#Potentially useful pieces of code worked out for special cases

#Delete all pre-existing rules with the same priority for a given input and output port
def delete_preexisitng(address, src_port, dst_port, username=None, password=None):
    uri_existing = 'http://' + address + '/rest/rules/all?'

    src_dst = []

    activerules = requests.get(uri_existing, auth=(username, password))
    existing = activerules.content
    load_existing = json.loads(existing)
    for item in load_existing['rules']:
        name = item['name']
        dest = re.findall('to ([0-9]+)', name)
        if dest[0] == src_port or dest[0] == dst_port:
            src_dst.append(item['name'][0])

    for port in src_dst:
        params_delete = {'priority': 32768,
                         'match[in_port]': port}
        try:
            delete_preexisting = requests.delete(uri_existing, params=params_delete, auth=(username, password))
        except ConnectionError as e:
            raise e

#Determine the total port count of an EX unit
def port_count(address, username=None, password=None):
    uri = 'http://' + address + '/rest/ports/config?'
    ports = list()
    try:
        response = requests.get(uri, auth=(username, password))
        r = response.content
        data = json.loads(r)
        count = 0
        for port in data['port_config']:
            ports.append(data['port_config'][count]['if_name'])
            count += 1
        return len(ports)
    except ConnectionError as e:
        raise e
