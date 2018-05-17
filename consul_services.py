import requests
import argparse
import json

def list_services(consul):
    path = "http://{}/v1/catalog/services".format(consul)
    r = requests.get(path)
    return r.json().keys()

def list_nodes(consul, service):
    path = "http://{}/v1/catalog/service/{}".format(consul, service)
    r = requests.get(path)
    nodes = [
                {
                    'Node': n['Node'],
                    'Datacenter': n['Datacenter'],
                    'ServiceAddress': n['ServiceAddress'],
                    'ServicePort': n['ServicePort'],
                    'Address': n['Address'],
                } \
            for n in r.json()]
    return nodes

def main():
    parser = argparse.ArgumentParser(description='Dump out list of services and nodes')
    parser.add_argument('--consul', dest='consul',
                    default='localhost:8500',
                    help='consul address (default: localhost:8500)')

    args = parser.parse_args()
    consul = args.consul
    services = list_services(consul)
    output = {}

    for service in services:
        nodes = list_nodes(consul, service)
        output[service] = nodes

    print json.dumps(output, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
