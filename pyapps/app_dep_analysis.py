# coding: utf-8

class Service(object):

    def __init__(self, id, name, dependencies: list):
        self.id = id
        self.name = name
        self.dependencies = dependencies

    def __str__(self):
        return f"[name={self.name},dep={self.dependencies}]"


class Analysis(object):

    def __init__(self, deploy_services: list, services_dep_table: dict):
        self._services_dep_table = services_dep_table
        self._deploy_services = self._create_deploy_services_list(
            deploy_services)

    def _create_deploy_services_list(self, svc_name_list) -> list:
        svc_list = []
        try:
            for name in svc_name_list:
                svc_list.append(self._services_dep_table[name])
        except KeyError as e:
            print('service not found:', e)
            exit(-1)

        sorted_svc_list = sorted(svc_list, key=lambda x: x.id)
        return [svc.name for svc in sorted_svc_list]

    def run(self) -> list:
        '''
        根据 发布服务列表 和 服务依赖关系，输出服务发布顺序。

        input:
        deploy_services: [g, e, c, a, x, d, b, h, f]
        services_dep_table: [a -> b], [c -> d,e], [d -> e], [f -> g -> h], [x]

        output:
        [b], [a -> b], [e], [d -> e], [c -> d,e], [h], [g -> h], [f -> g], [x]
        '''
        print('services to be deploy:', ','.join(self._deploy_services))

        ret_deploy_list = []
        while len(self._deploy_services) > 0:
            svc_name = self._deploy_services[0]
            self._handle_service(svc_name, ret_deploy_list)

        self._check_deploy_svc_list(ret_deploy_list, is_fix=True)
        return ret_deploy_list

    def _handle_service(self, svc_name, ret_deploy_list):
        svc = self._services_dep_table[svc_name]
        self._deploy_services.remove(svc_name)
        for dep_svc in svc.dependencies:
            if dep_svc in self._deploy_services:
                self._handle_service(dep_svc, ret_deploy_list)
        ret_deploy_list.append(svc)

    def _check_deploy_svc_list(self, deploy_svc_list, is_fix):
        '''
        检查依赖服务是否包含在服务发布列表中。
        '''
        deploy_svc_name_list = [svc.name for svc in deploy_svc_list]
        insert_dict = {}  # index:svc_name
        for idx in range(0, len(deploy_svc_list)):
            svc = deploy_svc_list[idx]
            for dep_svc_name in svc.dependencies:
                if dep_svc_name not in deploy_svc_name_list:
                    print(
                        f'for {svc}, its dependency service [{dep_svc_name}] NOT in deploy list.')
                    insert_dict[idx] = self._services_dep_table[dep_svc_name]

        if is_fix:
            self._fix_deploy_svc_list(deploy_svc_list, insert_dict)

    def _fix_deploy_svc_list(self, deploy_svc_list, fix_dict):
        '''
        服务发布列表中插入缺失的依赖服务，并根据依赖关系调整服务顺序。
        '''
        if len(fix_dict) == 0:
            return

        print('auto insert miss dependency services, and coordinate seq:')
        for idx, svc in fix_dict.items():
            print(svc.name)
            deploy_svc_list.insert(idx, svc)

            # fix dep services seq
            for svc_name in svc.dependencies:
                for s in deploy_svc_list:
                    if s.name == svc_name:
                        deploy_svc_list.remove(s)
                        deploy_svc_list.insert(idx, s)


def create_service_dep_table() -> dict:
    '''
    services_dep_table: [a -> b], [c -> d,e], [d -> e], [f -> g -> h], [x]

    注：依赖的服务排在后面，如服务b在a后面。
    '''
    service_dependencies_table = {}
    service_dependencies_table['a'] = Service(1, 'a', ['b'])
    service_dependencies_table['b'] = Service(2, 'b', [])
    # 依赖多个服务 [c -> d,e] [d -> e]
    service_dependencies_table['c'] = Service(3, 'c', ['d', 'e'])
    service_dependencies_table['d'] = Service(4, 'd', ['e'])
    service_dependencies_table['e'] = Service(5, 'e', [])
    # 多级依赖 [f -> g -> h]
    service_dependencies_table['f'] = Service(6, 'f', ['g'])
    service_dependencies_table['g'] = Service(7, 'g', ['h'])
    service_dependencies_table['h'] = Service(8, 'h', [])
    service_dependencies_table['x'] = Service(10, 'x', [])

    return service_dependencies_table


if __name__ == '__main__':

    # case1
    deploy_svc_list = ['g', 'e', 'a', 'x', 'd', 'b', 'h']
    svc_dep_table = create_service_dep_table()

    analysis = Analysis(deploy_svc_list, svc_dep_table)
    deploy_seq_list = analysis.run()
    print('servies to be deploy in seq:')
    for svc in deploy_seq_list:
        print(svc)

    # case2
    print()
    deploy_svc_list = ['g', 'e', 'c', 'a', 'x', 'd', 'b', 'h', 'f']
    analysis = Analysis(deploy_svc_list, svc_dep_table)
    deploy_seq_list = analysis.run()
    print('servies to be deploy in seq:')
    for svc in deploy_seq_list:
        print(svc)

    # case3, for [f -> g -> h], f and h are in deploy list, and g is NOT in.
    print()
    deploy_svc_list = ['e', 'c', 'a', 'x', 'd', 'b', 'h', 'f']
    analysis = Analysis(deploy_svc_list, svc_dep_table)
    deploy_seq_list = analysis.run()
    print('servies to be deploy in seq:')
    for svc in deploy_seq_list:
        print(svc)

    print('service dependencies analysis demo done.')
