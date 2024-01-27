from smbprotocol.connection import Connection
from smb.SMBConnection import (
    SMBConnection,
    OperationFailure,
    ProtocolError,
    NotConnectedError,
    SMBTimeout,
    NotReadyError,
)

import smbprotocol.exceptions
import threading
from logging import info, exception
import uuid

# ASCII color codes
green = '\033[32;3m'
yellow = '\033[33;3m'
fail = '\x1b[31;3m'
end = '\033[0m'


def smb_checker(host, port, timeout, dialects_int):
    index = 0
    count = {z: 0 for z in dialects_int}
    info(f'Starting... [SMB CHECK]: dict: {count} port: {port} timeout: {timeout}')
    x = host
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
                with open('samba/data/output.txt', 'a') as f:
                    f.write(f'{x}\n')
                    # f.write(f'{x}:{y}\n') with port
                break
        except (ValueError,
                TypeError) as err:
            print(f'{fail}[-]\t{end} [{x}] \t[0] : {err}, Dialect version: {y}')
            exception('Value or Type error')
            break
        except smbprotocol.exceptions.NotSupported as ex:
            print(f'{yellow}[!]\t{end} [{x}] \t[0] : {ex}, Dialect version int: {y}')
        except smbprotocol.exceptions.InvalidParameter as ex:
            print(f'{yellow}[!]\t{end} [{x}] \t[0] : {ex}, Dialect version: {y}')
        except (smbprotocol.exceptions.SMBConnectionClosed,
                smbprotocol.exceptions.SMBException) as ex:
            print(f'{fail}[-]\t{end} [{x}] \t[0] : {ex}, Dialect version: {y}')
            break


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
            with open('samba/data/all_shares.txt', 'a') as f:
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
                with open('samba/data/dump_dirs.txt', 'a') as f:
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
                exception(f'Two step error, please check {ip}')
    except TimeoutError as ex:
        print(f'Timeout: {ip}, {ex}')
    except (ProtocolError,
            NotConnectedError,
            SMBTimeout,
            NotReadyError,
            OSError):
        exception(f'First step error, please check {ip}')
    # This error need repair !!!
    except UnicodeEncodeError:
        exception(f'First step error, please check {ip}')
        pass


class SMBScanner:

    def __init__(self):
        self.port = 445
        self.timeout = 25
        self.dialects_int = [785, 770, 768, 528, 514, 767]

    # List = dialects version with integer
    def SMBDialectsScanner(self, samba_lib):
        print(f'\n{green}Starting{end} ---> Scanning dialects and probes samba protocol...')

        for ip in samba_lib:
            threading.Thread(target=smb_checker, args=(str(ip[0]), self.port, self.timeout, self.dialects_int)).start()

    def SMBDumpsDirsThreaded(self):
        print(f'\n{green}Starting{end} ---> Dumps all opened shares on hosts...')

        with open('samba/data/output.txt', 'r', encoding='utf-8') as ips:
            ips_library = [line.split("\n") for line in ips.read().splitlines()]

        for host in ips_library:
            threading.Thread(target=dumps_dir,
                             args=(str(host[0]), self.port, 'User', 'User', 'User', '.')).start()

    def SMBAllSharesThreaded(self):
        print(f'\n{green}Starting{end} ---> Check all hosts for list shares, without authentication...')

        with open('samba/data/output.txt', 'r', encoding='utf-8') as ips:
            ips_library = [line.split("\n") for line in ips.read().splitlines()]

        for host in ips_library:
            threading.Thread(target=smb_all_shares,
                             args=(str(host[0]), self.port, threading.active_count(), 'User', 'User', '.', 'Guest')).start()
