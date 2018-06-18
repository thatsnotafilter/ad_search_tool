from django.conf import settings
from ldap3 import Server, Connection, ALL, SYNC, SIMPLE, SUBTREE, ALL_ATTRIBUTES


class LDAPBackend(object):

    def __init__(self):

        self.domain = settings.AD_DNS_NAME
        self.s = Server(
            self.domain,
            port = 636,
            use_ssl = True,
            get_info = ALL
            )
        self.c = Connection(
            self.s,
            auto_bind = True,
            client_strategy = SYNC,
            user = settings.AD_USER,
            password = settings.AD_USER_PASSWORD,
            authentication = SIMPLE,
            check_names = True
            )



    def ldap_search(self, OUs, search_syntax):

        results = []
        
        search_results = self.c.extend.standard.paged_search(
            search_base = OUs,
            search_filter = search_syntax,
            search_scope = SUBTREE,
            attributes = ALL_ATTRIBUTES,
            paged_size = 5,
            generator = False
            )

            
        for entry in search_results:
            if 'attributes' in entry:
                results.append(entry['attributes'])
                    

        return results

