from pprint import pprint
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.
    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.
    Returns:
        A service that is connected to the specified API.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scopes)
    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)
    return service


def execute_request(service, property_uri, request):
    """Executes a searchAnalytics.query request.
    Args:
    service: The webmasters service to use when executing the query.
    property_uri: The site or app URI to request data for.
    request: The request to be executed.
    Returns:
    An array of response rows.
    """
    return service.searchanalytics().query(
        siteUrl=property_uri, body=request).execute()


def main():
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/webmasters.readonly'
    key_file_location = 'appleiwatch-0f78c5bb4aad.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='webmasters',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    working = True
    row_limit = 25000
    index = 0

    website = 'https://appleiwatch.name/'

    domain = website.split('/')[2].split('.')[0]

    f = open(f'{domain}_keys1.csv', 'w', encoding='utf-8')
    f.write(f"Page;Keyword;Impressions;Clicks;Position;Ctr\n")

    while working:
        request = {
            'startDate': '2020-01-01',
            'endDate': '2020-09-01',
            'dimensions': ['page', 'query'],
            # 'dimensionFilterGroups': [{
            #     'filters': [{
            #         'dimension': 'page',
            #         'expression': 'https://cools.com/shop/men?brand=blackbarrett'
            #     }],
            # }],
            # 'dimensions': ['date'],
            'rowLimit': row_limit,
            'startRow': row_limit * index
        }

        results = execute_request(
            service, website, request)

        if results.get('rows'):
            for row in results['rows']:
                try:
                    page = row['keys'][0]
                    keyword = row['keys'][1]
                    f.write(f"{page};{keyword};{row['impressions']};{row['clicks']};"
                            f"{row['position']};{row['ctr']}\n")
                except IndexError:
                    print(row['keys'], int(row['impressions']))

            index += 1
            pprint(results['rows'][:3])
        else:
            pprint(results)
            working = False


if __name__ == '__main__':
    main()
