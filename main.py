from smb.SMBConnection import (
    SMBConnection,
    OperationFailure,
    ProtocolError,
    NotConnectedError,
    SMBTimeout,
    NotReadyError,
)
from smbprotocol.connection import Connection

import smbprotocol.exceptions
import matplotlib.pyplot as plt
import threading
import logging
import numpy
import uuid


# ASCII color codes
green = '\033[32;3m'
yellow = '\033[33;3m'
fail = '\x1b[31;3m'
end = '\033[0m'


def smb_check(hosts, port, timeout, dialects_int):
    index = 0
    count = {z: 0 for z in dialects_int}
    logging.info(f'Starting... [SMB CHECK]: dict: {count} port: {port} timeout: {timeout}')
    for x in hosts:
        for y in dialects_int:
            try:
                conn = Connection(uuid.uuid4(), x, port)
                conn.connect(y, timeout)
                success = conn.disconnect()
                # Check string for messages, if message = None = SMB not open
                if success != '':
                    count[y] += 1
                    index += 1
                    print(f'{green}[+]\t{end} [{x}] \t[{index}] : {conn}, Dialect version: {y}')
                    with open('output/output.txt', 'a') as f:
                        f.write(f'{x}:{y}\n')
                    break
            except (ValueError,
                    TypeError) as err:
                print(f'{fail}[-]\t{end} [{x}] \t[0] : {err}, Dialect version: {y}')
                logging.exception('Value or Type error')
                break
            except smbprotocol.exceptions.NotSupported as ex:
                print(f'{yellow}[!]\t{end} [{x}] \t[0] : {ex}, Dialect version int: {y}')
            except smbprotocol.exceptions.InvalidParameter as ex:
                print(f'{yellow}[!]\t{end} [{x}] \t[0] : {ex}, Dialect version: {y}')
            except (smbprotocol.exceptions.SMBConnectionClosed,
                    smbprotocol.exceptions.SMBException) as ex:
                print(f'{fail}[-]\t{end} [{x}] \t[0] : {ex}, Dialect version: {y}')
                break

    # Creating bars for scanned versions dialects, using module matplotlib
    input(f'\nTap to create a diagram dialects...')
    version = (f'3.1.1\n[{count[785]}]', f'3.0.2\n[{count[770]}]', f'3.0.0\n[{count[768]}]',
               f'2.1.0\n[{count[528]}]', f'2.0.2\n[{count[514]}]', f'2.WILDCARD\n[{count[767]}]',)
    performance = [count[785], count[770], count[768], count[528], count[514], count[767], ]
    y_pos = numpy.arange(len(version))
    logging.info(f'Diagram created... all_count: {performance}')
    plt.bar(y_pos, performance, align='center', alpha=0.5, color='darkblue')
    plt.xticks(y_pos, version), plt.ylabel('Hosts'), plt.title('Dialect versions'), plt.show()


def smb_all_shares(ip, port, thr, username, password, domain, client_name):
    # Connecting on 445 port with smbprotocol module
    try:
        if port == 445:
            is_direct_tcp = True
        else:
            is_direct_tcp = False
        # Options to connect SMB module
        conn = SMBConnection(username, password, client_name,
                             ip, domain, use_ntlm_v2=True,
                             is_direct_tcp=is_direct_tcp)
        smb_auth_successful = conn.connect(ip, port, timeout=25)
        if smb_auth_successful:
            all_shares = conn.listShares(timeout=25)
            # Append all results for host
            lib = {}
            for i in range(len(all_shares)):
                lib[i] = all_shares[i].name
            with open('output/all_shares.txt', 'a') as f:
                f.write(f'{ip}:{lib}\n')
            print(f'{green}[+]{end} [SMB] [thr: {thr}] [{ip}]: '
                  f'{conn} Authentication successful: {yellow}[not checked] {lib}{end}')
        else:
            # Some errors may not display correctly, this is due to language conversion in folders
            print(f'{fail}[-]{end} [SMB] [thr: {thr}] [{ip}]: '
                  f'Authentication aborted, more:{yellow} Some errors may not display correctly, '
                  f'this is due to language conversion in folders{end}')
    except Exception as ex:
        print(f'{yellow}[!]{end} [SMB] [thr: {thr}] [{ip}]: Timeout from samba, more: {ex}')


def dumps_dir(ip, port, username, password, client, domain):
    try:
        conn = SMBConnection(username, password, client, ip, domain, use_ntlm_v2=True, is_direct_tcp=True)
        conn.connect(ip, port, timeout=25)
        shares = conn.listShares(timeout=25)
        lib_dir = list()
        for i in range(len(shares)):
            lib_dir.append(shares[i].name)
        for x in lib_dir:
            try:
                conn.listPath(x, '/')
                a_ = conn.listPath(x, '/', search=65591, pattern='*', timeout=20)
                lib_dir_v2 = list()
                for files in a_:
                    lib_dir_v2.append(files.filename)
                with open('output/dump_dirs.txt', 'a') as f:
                    f.write(f'{ip}:{x}:{lib_dir_v2[2:]}\n')
                print(f'{green}[+]{end} [{ip}] : {x} : {lib_dir_v2[2:5]} : More info on a file')
            except OperationFailure:
                print(f'{fail}[-]{end} [{ip}] : Authentication aborted on {x} ')
                pass
            except (ProtocolError,
                    NotConnectedError,
                    SMBTimeout,
                    NotReadyError,
                    OSError):
                logging.exception(f'Two step error, please check {ip}')
    except TimeoutError as ex:
        print(f'Timeout: {ip}, {ex}')
    except (ProtocolError,
            NotConnectedError,
            SMBTimeout,
            NotReadyError,
            OSError):
        logging.exception(f'First step error, please check {ip}')
    # This error need repair !!!
    except UnicodeEncodeError:
        logging.exception(f'First step error, please check {ip}')
        pass


def user_list():
    pass


if __name__ == '__main__':
    samba_lib = {
        '95.22.216.192', '95.23.90.102', '95.22.2.28', '213.133.99.210', '213.133.122.84',
    }
    # Logs for view some errors
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s')
    # List = dialects version with integer
    input()
    print(f'\n{green}Starting{end} ---> Scanning dialects and probes samba protocol...')
    smb_check(samba_lib, port=445, timeout=25, dialects_int=[785, 770, 768, 528, 514, 767])

    input()
    logging.info('Start scanning with [DUMPS DIRS ON SHARES SMB]...')
    print(f'\n{green}Starting{end} ---> Dumps all opened shares on hosts...')
    for ip in samba_lib:
        threading.Thread(target=dumps_dir,
                         args=(str(ip), 445, 'User', 'User', 'User', '.')).start()

    input()
    logging.info('Start scanning with [CHECK SHARES SMB]...')
    print(f'\n{green}Starting{end} ---> Check all hosts for list shares, without authentication...')
    for ip in samba_lib:
        port = 445
        threading.Thread(target=smb_all_shares,
                         args=(str(ip), port, threading.active_count(), 'User', 'User', '.', 'Guest')).start()
