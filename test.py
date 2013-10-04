import pexpect


def main():
    print 'Starting test for SeaGoat command line....'
    print
    print 'Starting server....'
    server = pexpect.spawn('./server.py')
    print 'Server started.'
    print
    print 'Starting client in command line...'
    client = pexpect.spawn('./client.py cli')
    client.expect('(Cmd)')
    print 'Client started.'
    
    print 'Killing client...'
    client.close()
    print 'Killed client.'
    print 'Killing server...'
    server.close()
    print 'Killed server.'
    
    print 'Tests done'

if __name__ == '__main__':
    main()