
class Host(object):
    
    def list_hostnames(self):
        pass


    def add_hostname(self, ip, canonical, alias=None):
        """ Add new hostname.
        
        @param ip: IP address
        @param canonical: Canonical address
        @param alias: One or more alias.
        
        @raise:
        """
        pass


    def delete_hostname(self, ip, canonical=None, alias=None, force=False):
        """ Delete hostname.

        @param ip: IP address
        @param canonical: Canonical address(optional).
        @param alias: One or more alias(optional).
        @param force: If more than one ip address is found remove all
                      default (False).
        
        @raise DuplicateEntryFound, :
        """
        pass