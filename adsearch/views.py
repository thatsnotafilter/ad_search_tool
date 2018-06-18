from django.conf import settings
from django.shortcuts import render
from adsearch import ldap, validator
from .forms import SearchForm



def index(request):

    results = []

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            
            # process the data in form.cleaned_data as required
            ldapbe = ldap.LDAPBackend()

            form_entry = form.cleaned_data['search_criteria']

            # mail and upn
            if '@' in form_entry:
                ldap_filter = [
                    '(mail={0})'.format(form_entry),
                    '(userPrincipalName={0})'.format(form_entry)
                    ]

            # firstname lastname or firstname middlename lastname
            elif form_entry.count(' ') == 1 or form_entry.count(' ') == 2:
                ldap_filter = [
                    '(displayName={0}*)'.format(form_entry),
                    '(cn={0}*)'.format(form_entry)
                ]

            else:
                # single-value search
                ldap_filter = [
                    '(sAMAccountName={0}*)'.format(form_entry),
                    '(sn={0}*)'.format(form_entry),
                    '(givenName={0}*)'.format(form_entry),
                ]

            for x in ldap_filter:
                for entry in ldapbe.ldap_search(settings.AD_BASE_DN, x):
                    if entry not in results:
                        results.extend([entry])

            if len(results) > 0:
                validate = validator.attr_validator()
                ad_search_results = validate.filter_user_attr(results)
                comments = validate.get_comments(results)
                    

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'index.html', {
        'form': form,
        'results': results,
        }
    )
