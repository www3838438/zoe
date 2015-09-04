conf = {
    'docker_swarm_manager': 'tcp://bf1.bigfoot.eurecom.fr:2380',
    'status_refresh_interval': 10,
    'scheduler_task_interval': 10,
    'db_connection': 'mysql+mysqlconnector://zoe:6sz2tfPuzBcCLdEz@m1.bigfoot.eurecom.fr/zoe',
    'redis_server': '192.168.45.2',
    'redis_port': '6379',
    'redis_db': 0,
    'apache-proxy-config-file': '/tmp/zoe-proxy.conf',
    'apache-log-file': '/var/log/apache2/access.log',
    'proxy_update_accesses': 300,
    'check_health': 30,
    'notebook_max_age_no_activity': 24,
    'notebook_warning_age_no_activity': 2,
    'email_task_interval': 300,
    'client_rpyc_autodiscovery': True,
    'client_rpyc_server': None,
    'client_rpyc_port': None,
    'proxy_path_prefix': '/proxy',
    'smtp_server': 'smtp.gmail.com',
    'smtp_user': 'bigfoot.data@gmail.com',
    'smtp_pass': open('smtp_pass.txt', 'r').read().strip(),
    'web_server_name': 'bigfoot-m2.eurecom.fr'
}
