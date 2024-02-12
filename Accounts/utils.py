def prepareUpdatedData(data, user_id):
    """
    Prepares the update data with optional fields.

    :param user_id:
    :param data: The parsed JSON data from the request body.
    :return: A dictionary with fields that are present in the input data.
    """
    updatedData = {'id': user_id}

    # Only include fields in update_data if they are present in the request
    if 'username' in data:
        updatedData['username'] = data['username']
    if 'email' in data:
        updatedData['email'] = data['email']
    if all(k in data for k in ('oldPassword', 'password', 'passwordConfirm')):
        updatedData['oldPassword'] = data['oldPassword']
        updatedData['password'] = data['password']
        updatedData['passwordConfirm'] = data['passwordConfirm']
    # Add more fields as necessary

    return updatedData
