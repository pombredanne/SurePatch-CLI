import json
import re


def get_composer_content():
    with open('c:\\composer1.json') as f:
        return json.load(f)


def get_names_and_versions_packages():
    content = get_composer_content()

    packages = []
    for key in content:
        if key == 'require' or key == 'require-dev':
            for inner_key, value in content[key].items():
                if '/' in inner_key:
                    package_name = inner_key.split('/')[1]
                else:
                    package_name = inner_key

                if '||' in value:
                    splitted_values = value.split('||')
                elif '|' in value:
                    splitted_values = value.split('|')
                else:
                    splitted_values = value.split(',')

                for splitted_value in splitted_values:
                    package = {
                        'name': '*',
                        'version': '*'
                    }

                    version = re.findall(r'(\d.*)', splitted_value)

                    if version:
                        package['name'] = package_name
                        package['version'] = version[0].lstrip().rstrip()
                        packages.append(package)

    formed_packages = []
    buff_packages = []
    for package in packages:
        buff_package = {
            'name': '*',
            'version': '*',
            'origin_version': '*'
        }

        splitted_packages_by_dot = package['version'].split('.')

        if len(splitted_packages_by_dot) == 1:
            buff_package['name'] = package['name']
            buff_package['origin_version'] = package['version']

            package['version'] = '{}.0.0'.format(splitted_packages_by_dot[0])
            formed_packages.append(package)

            buff_package['version'] = package['version']
            buff_packages.append(buff_package)
        elif len(splitted_packages_by_dot) == 2:
            buff_package['name'] = package['name']
            buff_package['origin_version'] = package['version']

            package['version'] = '{}.{}.0'.format(splitted_packages_by_dot[0], splitted_packages_by_dot[1])
            formed_packages.append(package)

            buff_package['version'] = package['version']
            buff_packages.append(buff_package)
        else:
            formed_packages.append(package)

    unique_packages = []
    for i in range(len(formed_packages)):
        package = formed_packages.pop()

        if package not in unique_packages:
            unique_packages.append(package)

    for package in unique_packages:
        for buff_package in buff_packages:
            if package['name'] == buff_package['name'] and package['version'] == buff_package['version']:
                package['version'] = buff_package['origin_version']

    return unique_packages


ps = get_names_and_versions_packages()

for p in ps:
    print(p)
