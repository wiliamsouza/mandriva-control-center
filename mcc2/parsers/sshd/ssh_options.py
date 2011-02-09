'''
Created on Jan 27, 2011

@author: guilherme
'''

class SSHDOptions(object):
    '''
    Wrapper for all config options
    '''
    
    ACCEPTENV = 'AcceptEnv'
    ADDRESSFAMILY = 'AddressFamily'
    ALLOWAGENTFORWARDING = 'AllowAgentForwarding'
    ALLOWGROUPS = 'AllowGroups'
    ALLOWTCPFORWARDING = 'AllowTcpForwarding'
    ALLOWUSERS = 'AllowUsers'
    AUTHORIZEDKEYSFILE = 'AuthorizedKeysFile'
    AUTHORIZEDPRINCIPALSFILE = 'AuthorizedPrincipalsFile'
    BANNER = 'Banner'
    CHALLENGERESPONSEAUTHENTICATION = 'ChallengeResponseAuthentication'
    CHROOTDIRECTORY = 'ChrootDirectory'
    CIPHERS = 'Ciphers'
    CLIENTALIVEINTERVAL = 'ClientAliveInterval'
    COMPRESSION = 'Compression'
    DENYGROUPS = 'DenyGroups'
    DENYUSERS = 'DenyUsers'
    FORCECOMMAND = 'ForceCommand'
    GSSAPIAUTHENTICATION = 'GSSAPIAuthentication'
    GSSAPICLEANUPCREDENTIALS = 'GSSAPICleanupCredentials'
    GATEWAYPORTS = 'GatewayPorts'
    HOSTCERTIFICATE = 'HostCertificate'
    HOSTKEY = 'HostKey'
    HOSTBASEDAUTHENTICATION = 'HostbasedAuthentication'
    HOSTBASEDUSESNAMEFROMPACKETONLY = 'HostbasedUsesNameFromPacketOnly'
    IGNORERHOSTS = 'IgnoreRhosts'
    IGNOREUSERKNOWNHOSTS = 'IgnoreUserKnownHosts'
    KERBEROSAUTHENTICATION = 'KerberosAuthentication'
    KERBEROSGETAFSTOKEN = 'KerberosGetAFSToken'
    KERBEROSORLOCALPASSWD = 'KerberosOrLocalPasswd'
    KERBEROSTICKETCLEANUP = 'KerberosTicketCleanup'
    KEYREGENERATIONINTERVAL = 'KeyRegenerationInterval'
    LISTENADDRESS = 'ListenAddress'
    LOGLEVEL = 'LogLevel'
    LOGINGRACETIME = 'LoginGraceTime'
    MACS = 'MACs'
    MATCH = 'Match'
    MAXAUTHTRIES = 'MaxAuthTries'
    MAXSESSIONS = 'MaxSessions'
    MAXSTARTUPS = 'MaxStartups'
    PASSWORDAUTHENTICATION = 'PasswordAuthentication'
    PERMITEMPTYPASSWORDS = 'PermitEmptyPasswords'
    PERMITOPEN = 'PermitOpen'
    PERMITROOTLOGIN = 'PermitRootLogin'
    PERMITTUNNEL = 'PermitTunnel'
    PERMITUSERENVIRONMENT = 'PermitUserEnvironment'
    PIDFILE = 'PidFile'
    PORT = 'Port'
    PRINTLASTLOG = 'PrintLastLog'
    PRINTMOTD = 'PrintMotd'
    PROTOCOL = 'Protocol'
    PUBKEYAUTHENTICATION = 'PubkeyAuthentication'
    RSAAUTHENTICATION = 'RSAAuthentication'
    REVOKEDKEYS = 'RevokedKeys'
    RHOSTSRSAAUTHENTICATION = 'RhostsRSAAuthentication'
    SERVERKEYBITS = 'ServerKeyBits'
    STRICTMODES = 'StrictModes'
    SUBSYSTEM = 'Subsystem'
    SYSLOGFACILITY = 'SyslogFacility'
    TCPKEEPALIVE = 'TCPKeepAlive'
    TRUSTEDUSERCAKEYS = 'TrustedUserCAKeys'
    USEDNS = 'UseDNS'
    USELOGIN = 'UseLogin'
    USEPAM = 'UsePAM'
    X11DISPLAYOFFSET = 'X11DisplayOffset'
    X11FORWARDING = 'X11Forwarding'
    X11USELOCALHOST = 'X11UseLocalhost'
    XAUTHLOCATION = 'XAuthLocation'

    
    options_list = ['AcceptEnv',
         'AddressFamily',
         'AllowAgentForwarding',
         'AllowGroups',
         'AllowTcpForwarding',
         'AllowUsers',
         'AuthorizedKeysFile',
         'AuthorizedPrincipalsFile',
         'Banner',
         'ChallengeResponseAuthentication',
         'ChrootDirectory',
         'Ciphers',
         'ClientAliveInterval',
         'Compression',
         'DenyGroups',
         'DenyUsers',
         'ForceCommand',
         'GatewayPorts',
         'GSSAPIAuthentication',
         'GSSAPICleanupCredentials',
         'HostbasedAuthentication',
         'HostbasedUsesNameFromPacketOnly',
         'HostCertificate',
         'HostKey',
         'IgnoreRhosts',
         'IgnoreUserKnownHosts',
         'KerberosAuthentication',
         'KerberosGetAFSToken',
         'KerberosOrLocalPasswd',
         'KerberosTicketCleanup',
         'KeyRegenerationInterval',
         'ListenAddress',
         'LoginGraceTime',
         'LogLevel',
         'MACs',
         'Match',
         'MaxAuthTries',
         'MaxSessions',
         'MaxStartups',
         'PasswordAuthentication',
         'PermitEmptyPasswords',
         'PermitOpen',
         'PermitRootLogin',
         'PermitTunnel',
         'PermitUserEnvironment',
         'PidFile',
         'Port',
         'PrintLastLog',
         'PrintMotd',
         'Protocol',
         'PubkeyAuthentication',
         'RevokedKeys',
         'RhostsRSAAuthentication',
         'RSAAuthentication',
         'ServerKeyBits',
         'StrictModes',
         'Subsystem',
         'SyslogFacility',
         'TCPKeepAlive',
         'TrustedUserCAKeys',
         'UseDNS',
         'UseLogin',
         'UsePAM',
         'UsePrivilegeSeparation',
         'X11DisplayOffset',
         'X11Forwarding',
         'X11UseLocalhost',
         'XAuthLocation']
    options_dict = {'AcceptEnv': 'AcceptEnv',
             'AddressFamily': 'AddressFamily',
             'AllowAgentForwarding': 'AllowAgentForwarding',
             'AllowGroups': 'AllowGroups',
             'AllowTcpForwarding': 'AllowTcpForwarding',
             'AllowUsers': 'AllowUsers',
             'AuthorizedKeysFile': 'AuthorizedKeysFile',
             'AuthorizedPrincipalsFile': 'AuthorizedPrincipalsFile',
             'Banner': 'Banner',
             'ChallengeResponseAuthentication': 'ChallengeResponseAuthentication',
             'ChrootDirectory': 'ChrootDirectory',
             'Ciphers': 'Ciphers',
             'ClientAliveInterval': 'ClientAliveInterval',
             'Compression': 'Compression',
             'DenyGroups': 'DenyGroups',
             'DenyUsers': 'DenyUsers',
             'ForceCommand': 'ForceCommand',
             'GSSAPIAuthentication': 'GSSAPIAuthentication',
             'GSSAPICleanupCredentials': 'GSSAPICleanupCredentials',
             'GatewayPorts': 'GatewayPorts',
             'HostCertificate': 'HostCertificate',
             'HostKey': 'HostKey',
             'HostbasedAuthentication': 'HostbasedAuthentication',
             'HostbasedUsesNameFromPacketOnly': 'HostbasedUsesNameFromPacketOnly',
             'IgnoreRhosts': 'IgnoreRhosts',
             'IgnoreUserKnownHosts': 'IgnoreUserKnownHosts',
             'KerberosAuthentication': 'KerberosAuthentication',
             'KerberosGetAFSToken': 'KerberosGetAFSToken',
             'KerberosOrLocalPasswd': 'KerberosOrLocalPasswd',
             'KerberosTicketCleanup': 'KerberosTicketCleanup',
             'KeyRegenerationInterval': 'KeyRegenerationInterval',
             'ListenAddress': 'ListenAddress',
             'LogLevel': 'LogLevel',
             'LoginGraceTime': 'LoginGraceTime',
             'MACs': 'MACs',
             'Match': 'Match',
             'MaxAuthTries': 'MaxAuthTries',
             'MaxSessions': 'MaxSessions',
             'MaxStartups': 'MaxStartups',
             'PasswordAuthentication': 'PasswordAuthentication',
             'PermitEmptyPasswords': 'PermitEmptyPasswords',
             'PermitOpen': 'PermitOpen',
             'PermitRootLogin': 'PermitRootLogin',
             'PermitTunnel': 'PermitTunnel',
             'PermitUserEnvironment': 'PermitUserEnvironment',
             'PidFile': 'PidFile',
             'Port': 'Port',
             'PrintLastLog': 'PrintLastLog',
             'PrintMotd': 'PrintMotd',
             'Protocol': 'Protocol',
             'PubkeyAuthentication': 'PubkeyAuthentication',
             'RSAAuthentication': 'RSAAuthentication',
             'RevokedKeys': 'RevokedKeys',
             'RhostsRSAAuthentication': 'RhostsRSAAuthentication',
             'ServerKeyBits': 'ServerKeyBits',
             'StrictModes': 'StrictModes',
             'Subsystem': 'Subsystem',
             'SyslogFacility': 'SyslogFacility',
             'TCPKeepAlive': 'TCPKeepAlive',
             'TrustedUserCAKeys': 'TrustedUserCAKeys',
             'UseDNS': 'UseDNS',
             'UseLogin': 'UseLogin',
             'UsePAM': 'UsePAM',
             'X11DisplayOffset': 'X11DisplayOffset',
             'X11Forwarding': 'X11Forwarding',
             'X11UseLocalhost': 'X11UseLocalhost',
             'XAuthLocation': 'XAuthLocation'}
