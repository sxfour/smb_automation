from smbprotocol.connection import Connection
from subprocess import Popen, PIPE
from postgresql import AddHosts
import smbprotocol.exceptions
from smb.SMBConnection import (
    SMBConnection,
    OperationFailure,
    ProtocolError,
    NotConnectedError,
    SMBTimeout,
    NotReadyError,
)

import uuid

# ASCII color codes
green = '\033[32;3m'
yellow = '\033[33;3m'
fail = '\x1b[31;3m'
end = '\033[0m'


def get_pipe():
    args = ['sudo', 'masscan', '84.0.0.0-98.255.255.255', '-p', '445', '--rate', '250', '--connection-timeout', '8']
    process = Popen(args, stdout=PIPE)
    dialects = [785, 770, 768, 528, 514, 767]

    for line in process.stdout:
        host = line.decode('cp866').split()
        try:
            smb_checker(str(host[5]), 445, 25, dialects)
        except Exception as ex:
            print(f'{fail}{ex}{end}')

    data, error = process.communicate()

    print(error)

    return data.decode(encoding='cp866')


def startPipe():
    print(get_pipe())
    input()


def dumps_dir(ip, port, username, password, client, domain):
    try:
        conn = SMBConnection(username, password, client, ip, domain, use_ntlm_v2=True, is_direct_tcp=True)
        conn.connect(ip, port, timeout=25)
        shares = conn.listShares(timeout=25)
        lib_dir = list()
        string = ''
        for i in range(len(shares)):
            lib_dir.append(shares[i].name)
        for x in lib_dir:
            try:
                conn.listPath(x, '/')
                a_ = conn.listPath(x, '/', search=65591, pattern='*', timeout=20)
                lib_dir_v2 = list()
                for files in a_:
                    lib_dir_v2.append(files.filename)
                print(f'{green}[+]{end} [{ip}] : {x} : {lib_dir_v2[2:5]} : More info on a file')
            except OperationFailure:
                print(f'{fail}[-]{end} [{ip}] : Authentication aborted on {x} ')
                pass
            except (ProtocolError, NotConnectedError, SMBTimeout, NotReadyError, OSError):
                print(f'Two step error, please check {ip}')

        # List dirs to string
        for el in lib_dir:
            string += str(el)
            string += '/'
        # Create PostgreSQL request to add all found information
        AddHosts().appendHostPostgreSQL(ip, port, username, password, string)

    except TimeoutError as ex:
        print(f'{fail}[-]{end} Timeout: {ip}, {ex} ')
    except (ProtocolError, NotConnectedError, SMBTimeout, NotReadyError, OSError):
        print(f'{fail}[-]{end} First step error, please check {ip} ')

    # This error need repair !!!
    except UnicodeEncodeError:
        print(f'{fail}[-]{end} First step error, please check {ip} ')


def smb_checker(host, port, timeout, dialects_int):
    count = {z: 0 for z in dialects_int}
    x = host
    for y in dialects_int:
        try:
            conn = Connection(uuid.uuid4(), x, port)
            conn.connect(y, timeout)
            success = conn.disconnect()

            # Check string for messages, if message = None = SMB not open
            if success != '':
                count[y] += 1
                print(f'{green}[+]\t{end} [{x}] \t[0] : {conn}, Dialect version: {y}')
                dumps_dir(str(host), port, 'User', 'User', 'Guest', '.')
                break

        except (ValueError, TypeError) as err:
            # print(f'{fail}[-]\t{end} [{x}] \t[0] : {err}, Dialect version: {y}')
            break
        except smbprotocol.exceptions.NotSupported as ex:
            # print(f'{yellow}[!]\t{end} [{x}] \t[0] : {ex}, Dialect version int: {y}')
            pass
        except smbprotocol.exceptions.InvalidParameter as ex:
            pass
            # print(f'{yellow}[!]\t{end} [{x}] \t[0] : {ex}, Dialect version: {y}')
        except (smbprotocol.exceptions.SMBConnectionClosed, smbprotocol.exceptions.SMBException) as ex:
            # print(f'{fail}[-]\t{end} [{x}] \t[0] : {ex}, Dialect version: {y}')
            break


if __name__ == '__main__':
    startPipe()
