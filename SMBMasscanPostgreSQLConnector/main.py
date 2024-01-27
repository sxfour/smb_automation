from samba.connector.smb_check import SMBScanner
# from subprocess import Popen, PIPE
from postgresql import AddHosts

from logging import basicConfig, INFO


# def get_pipe():
#     args = ['sudo', 'masscan', '178.30.0.0-178.40.0.0', '-p', '445', '--rate', '200', '--connection-timeout', '4']
#     process = Popen(args, stdout=PIPE)
#
#     for line in process.stdout:
#         host = line.decode('cp866').split()
#
#         # AddHosts().infoPostgreSQL()
#         AddHosts().appendHostPostgreSQL(host)
#
#         print(host)
#
#     data, error = process.communicate()
#
#     print(error)
#
#     return data.decode(encoding='cp866')
#
#
# def startPipe():
#     print(get_pipe())
#     input()


if __name__ == '__main__':
    # startPipe()
    # AddHosts().infoPostgreSQL()

    basicConfig(level=INFO, filename='samba/logs/logs.log', filemode='w',
                format='%(asctime)s %(levelname)s %(message)s')

    # Threaded dialects version dirs
    input()
    SMBScanner().SMBDialectsScanner(samba_lib=AddHosts().allHostsPostgreSQL())

    # Threaded Check all dirs without auth check
    input()
    SMBScanner().SMBAllSharesThreaded()

    # Threaded scanner share and dirs with User auth
    input()
    SMBScanner().SMBDumpsDirsThreaded()
