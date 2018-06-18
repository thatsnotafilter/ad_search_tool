from datetime import datetime, timezone, timedelta
from django.conf import settings

class attr_validator(object):
        

    def without_keys(self, d, keys):
        
        return {x: d[x] for x in d if x not in keys}
    

    def filter_user_attr(self, results):

        # attributes to be filtered out
        not_wanted_attrs = [
            'userCertificate',
            ]

        filtered_results = []

        for result in results:
            filtered_results.append(self.without_keys(result, not_wanted_attrs))

        return filtered_results


    def get_comments(self, results):

        # probably problematic user attributes and values
        usr_problem_attrs_and_values = {
            'userAccountControl':[514, 546, 66048, 66050, 66082, 262658, 262690, 328194, 328226],
        }
        # probably problematic user attributes and values
        wks_problem_attrs_and_values = {
            'userAccountControl':[4098],
        }

        # common user attributes that often require a closer look
        usr_problem_attrs = [
            'accountExpires',
            'pwdLastSet',
            ]

        comments = []

        for result in results:
            if 'computer' in result['objectClass']:
                for key, value in result.items():
                    if key in wks_problem_attrs_and_values and value in wks_problem_attrs_and_values[key]:
                        if key == 'userAccountControl':
                            comments.append('computer object is locked (userAccountControl)')

            elif 'computer' not in result['objectClass'] and 'user' in result['objectClass']:
                for key, value in result.items():
                    if key in usr_problem_attrs_and_values and value in usr_problem_attrs_and_values[key]:
                        if key == 'userAccountControl':
                            if value == 546:
                                comments.append('user account is locked (userAccountControl)')
                            else:
                                comments.append('user accunt is not NORMAL ACCOUNT (userAccountControl)')
                    elif key in usr_problem_attrs:
                        if key == 'accountExpires':
                            if value == datetime(9999, 12, 31, 23, 59, 59, 999999):
                                comments.append('user account never expires (accountExpires)')
                            elif value == datetime(1601, 1, 1, 00, 00, 00, tzinfo=timezone.utc):
                                comments.append('user account never expires (accountExpires)')
                            elif value < datetime.now(timezone.utc):
                                comments.append('user account has expired (accountExpires)')
                        elif key == 'pwdLastSet':
                            expiry_date = value + timedelta(days = settings.PASSWORD_AGE_MAX)
                            if expiry_date < datetime.now(timezone.utc):
                                comments.append('password has expired {0} (pwdLastSet)'.format(expiry_date.strftime('%Y-%m-%d %I:%M')))
                            if expiry_date > datetime.now(timezone.utc):
                                comments.append('password expires {0}'.format(expiry_date.strftime('%Y-%m-%d %I:%M')))
                            if value > datetime.now(timezone.utc) - timedelta(hours = 24):
                                comments.append('password is less than 24 hours old (pwdLastSet)')

                                

            if len(comments) > 0:
                result['comments'] = comments
                comments = []


        return results
                        

        
