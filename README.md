# OneLogin Python SDK

This SDK will let you execute all the API methods, version/1, described
at https://developers.onelogin.com/api-docs/1/getting-started/dev-overview.

## Installation
### Hosting
#### Github
The toolkit is hosted on github. You can download it from:
* Lastest release: https://github.com/onelogin/onelogin-python-sdk/releases/latest
* Master repo: https://github.com/onelogin/onelogin-python-sdk/tree/master

#### pypi
The toolkit is hosted in pypi, you can find the package at https://pypi.python.org/pypi/onelogin

You can install it executing:
```
$ pip install onelogin
```

If you want to know how a project can handle python packages review this [guide](https://packaging.python.org/en/latest/tutorial.html) and review this [sampleproject](https://github.com/pypa/sampleproject)


### Dependencies
onelogin-python-sdk works on Python2 or Python 3. It has the following dependencies:

* requests
* defusedxml
* python-dateutil


## Getting started

You'll need a OneLogin account and a set of API credentials before you get started. 

If you don't have an account you can [sign up for a free developer account here](https://www.onelogin.com/developer-signup).

|||
|---|---|
|client_id|Required: A valid OneLogin API client_id|   
|client_secret|Required: A valid OneLogin API client_secret|   
|region| Optional: `us` or `eu`. Defaults to `us`   |   

```python
from onelogin.api.client import OneLoginClient

client = OneLoginClient(
    client_id, 
    client_secret,
    region
)

#Now you can make requests 
client.get_rate_limits()
```

For all methods see Pydoc of this SDK published at:
https://onelogin.github.io/onelogin-python-sdk/index.html


## Usage

### Errors and exceptions

OneLogin's API can return 400, 401, 403 or 404 when there was any issue executing the action. When that happens, the methods of the SDK will include error and errorMessage in the OneLoginClient. Use the getError() and the getErrorDescription() to retrieve them.


### Authentication

By default methods call internally to `get_access_token` if there is no valid access_token. You can also get tokens etc directly if needed. 

```ruby
# Get an AccessToken
token = client.get_access_token()

# Refresh an AccessToken
token2 = client.regenerate_token()

# Revoke an AccessToken
token3 = client.get_access_token()
```

### Paging

All OneLogin API endpoints that support paging are returned as a Cursor object to save you keeping track of the paging cursor, you can retrieve the related objects by calling objects()

eg

```python
# List the first name of all users
for user in client.get_users().objects():
    print user.firstname

# List the first name of all users starting with the 2nd user
for user in client.get_users().objects()[1:]:
    print user.firstname

# List the first 5 users with the name of Joe
query_parameters = {'firstname': 'Joe'}
for user in client.get_users(query_parameters, max_results=5).objects():
    print user.firstname

# Get 10 event ids
ids = [user.id for user in client.get_events(max_results=10).objects()]

# Get all roles
client.get_roles().objects()
```

Here is an example of how use the Cursor object.

```python
# Limit the number of objects in page to 10
query_parameters = {'limit': 10}

# Retrieve the 40 events
cursor = client.get_events(max_results=40, query_parameters=query_parameters)
events = cursor.objects()
# Check that there are more events by verify that the after_cursor is not empty
after_cursor = cursor.get_after_cursor()
if after_cursor is not None:
    # Adding the after_cursor parameter to the query so next call to get_events
    # will start on the latest page previously processed
    query_parameters['after_cursor'] = after_cursor
    cursor = client.get_events(max_results=40, query_parameters=query_parameters)
    other_40_events = cursor.objects()
    events += other_40_events
```

An alternative is to use the fetch_again method, that method will execute
the same query that the cursor did when was initializated but starting in the next page processed by the cursor.

```python
query_parameters = {'limit': 10}
cursor = client.get_events(max_results=40, query_parameters=query_parameters)
# Retrieve 40 events
events = cursor.objects()
# Retrieve another 40 events
events += cursor.fetch_again().objects()
```

Make sure max_results is a multiple value of limit (if limit is not provided, a default value of 50 is used) or you can lost elements to be collected)
eg.

```python
query_parameters = {'limit': 4}
cursor = client.get_events(max_results=6, query_parameters=query_parameters)
# Retrieve the first six events (4 of the 1st page, 2 of the 2nd page),
# the last 2 events of 2nd page are not retrieved.
events = cursor.objects()
# Retrieve six new events, (4 of the 3rd page, 2 of the 4rd page)
events += cursor.fetch_again().objects()
```

### Available Methods

```python
# Get rate limits
rate_limits = client.get_rate_limits()

# Get Custom Attributes
custom_global_attributes = client.get_custom_attributes()

# Get Users with no query parameters
users = client.get_users().objects()

# Get Users with query parameters
query_parameters = {
    "email": "user@example.com"
}
users_filtered = client.get_users(query_parameters).objects()

query_parameters = {
    "email": "usermfa@example.com"
}
users_filtered2 = client.get_users(query_parameters).objects()

# Get Users with limit
query_parameters = {
    "limit": 3
}
users_filtered_limited = client.get_users(query_parameters).objects()

# Get User by id
user = client.get_user(users_filtered[0].id)
user_mfa = client.get_user(users_filtered2[0].id)

# Update User with specific id
user = client.get_user(user.id)
update_user_params = user.get_user_params()
update_user_params["firstname"] = 'modified_firstname'
user = client.update_user(user.id, update_user_params)
user = client.get_user(user.id)

# Get Global Roles
roles = client.get_roles().objects();

# Get Role
role = client.get_role(roles[0].id)
role2 = client.get_role(roles[1].id)

# Assign & Remove Roles On Users
role_ids = [
    role.id,
    role2.id 
]
result = client.assign_role_to_user(user.id, role_ids)
role_ids.pop()
result = client.remove_role_from_user(user.id, role_ids)
user = client.get_user(user.id)

# Sets Password by ID Using Cleartext
password = "Aa765431-XxX"
result = client.set_password_using_clear_text(user.id, password, password);

# Sets Password by ID Using Salt and SHA-256
password = "Aa765432-YyY";
salt = "11xxxx1";
import hashlib
hashed_salted_password = hashlib.sha256(salt + password).hexdigest()
result = client.set_password_using_hash_salt(user_mfa.id, hashed_salted_password, hashed_salted_password, "salt+sha256", salt);

 Set Custom Attribute Value to User
customAttributes = {
    custom_global_attributes[0]: "xxxx",
    custom_global_attributes[1]: "yyyy"
}
result = client.set_custom_attribute_to_user(34687020, customAttributes);

# Log Out User
result = client.log_user_out(user.id);

# Lock User
result = client.lock_user(user.id, 5);

# Get User apps
apps = client.get_user_apps(user.id)

# Get User Roles
role_ids = client.get_user_roles(user.id)

# Create user
new_user_params = {
    "email": "testcreate_1@example.com",
    "firstname": "testcreate_1_fn",
    "lastname": "testcreate_1_ln",
    "username": "testcreate_1@example.com"
}
created_user = client.create_user(new_user_params)

# Delete User
result = client.delete_user(created_user.id)

# Create Session Login Token
session_login_token_params = {
    "username_or_email": "user@example.com",
    "password": "Aa765431-XxX",
    "subdomain": "example-onelogin-subdomain"
}
session_token_data = client.create_session_login_token(session_login_token_params);

# Create Session Login Token MFA , after verify
session_login_token_mfa_params = {
    "username_or_email": "usermfa@example.com",
    "password": "Aa765432-YyY",
    "subdomain": "example-onelogin-subdomain"
}
session_token_mfa_data = client.create_session_login_token(session_login_token_mfa_params)
otp_token = "000000"; // We may take that value from OTP device
session_token_data2 = client.get_session_token_verified(session_token_mfa_data.devices[0].id, session_token_mfa_data.state_token, otp_token);

# Get EventTypes
event_types = client.get_event_types()

# Get Events
events = client.get_events()

query_events_params = {
    'limit': 2
}
events_limited = client.get_events(query_events_params)

# Get Event
event = client.get_event(events[0].id)

# Create Event
new_event_params = {
    "event_type_id": "000",
    "account_id": "00000",
    "actor_system": "00",
    "user_id": "00000000",
    "user_name": "test_event",
    "custom_message": "test creating event from python :)"
}
result = client.create_event(new_event_params)

# Get Filtered Events
query_events_params = array(
  "user_id": "00000000"
);
events = client.get_events(query_events_params);

# Get Groups
groups = client.get_groups().objects()

# Get Group
group = client.get_group(groups[0].id)

# Get SAMLResponse directly
app_id = "000000"
saml_endpoint_response = client.get_saml_assertion("user@example.com", "Aa765431-XxX", app_id, "example-onelogin-subdomain");

# Get SAMLResponse after MFA
saml_endpoint_response2 = client.get_saml_assertion("usermfa@example.com", "Aa765432-YyY", app_id, "example-onelogin-subdomain");
mfa = saml_endpoint_response2.mfa
otp_token = "000000";
saml_endpoint_response_after_verify = client.get_saml_assertion_verifying(app_id, mfa.devices[0].id, mfa.state_token, "78395727", None);

# Generate Invite Link
url_link = client.generate_invite_link("user@example.com")

# Send Invite Link
sent = client.send_invite_link("user@example.com")

#Get Apps to Embed for a User
embed_token = "30e256c101cd0d2e731de1ec222e93c4be8a1572"
apps = client.get_embed_apps("30e256c101cd0d2e731de1ec222e93c4be8a1572", "user@example.com")
```

## Development

After checking out the repo, run `pip setup install` or `python setup.py develop` to install dependencies. Then, run `pip setup test` to run the tests.

To release a new version, update the version number in `src/onelogin/api/version.py` and commit it, then you will be able to update it to pypy.
with `python setup.py sdist upload` and `python setup.py bdist_wheel upload`.
Create also a relase tag on github.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/onelogin/onelogin-ruby-sdk. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

## License

The gem is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

## Code of Conduct

Everyone interacting in the OneLogin Python SDK project’s codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/onelogin/onelogin-ruby-sdk/blob/master/CODE_OF_CONDUCT.md).