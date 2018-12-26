wrong_title = "Please provide a title of with string characters only"
wrong_description = "Please provide a description of type string"
wrong_comment = "Please provide a comment or type string"
wrong_video = "Please provide a list of a MP4 Videos or an empty list if none"
wrong_Images = "Please provide a list of JPEG Images or an empty list if none"
wrong_tags = "Please provide a list of string tags or an empty list if none"
wrong_location = (
    "location must contain a both Latitude and Longitude coordinates and "
    "latitude must be between -90 and 90 "
    "and longitude between -180 and 180"
)
expected_new_incident_format = {
    "title": "string",
    "description": "String",
    "location": [13.66, 89.98],
    "tags": [],
    "Videos": [],
    "Images": [],
}

wrong_password = (
    "Password Must contain a Minimum 8 characters with atleast one upper case"
    " letter, atleast on lower case letter and  atleast one number."
)

wrong_username = (
    "Username must be string with atleast 5 characters and may" " contain a number"
)
wrong_phone_number = "Phone number must be a string of ten digits only"
wrong_email = "Please provide a valid email address"
wrong_name = "Name field is a string and cannot be blank or contain a space or a number"
duplicate_email = "Account with specified email address already exists"
duplicate_user_name = "Username already exists"
delete_not_allowed = "You are not allowed to delete this resource"
red_flag_deleted = "red-flag record has been deleted"
supported_end_points = [
    "POST /auth/signup",
    "POST /auth/login",
    "GET /red-flags",
    "GET /red-flags/<red-flag-id>",
    "PATCH /red-flags/<red-flag-id>/location",
    "PATCH /red-flags/<red-flag-id>/comment",
    "DELETE /red-flags/<red-flag-id> - Delete a redflag",
]
