from datetime import datetime

from api.helpers import get_current_identity


class Incident:

    def __init__(self, **kwargs):
        self.id = None
        self.location = kwargs['location']
        self.Images = []
        self.Videos = []
        self.createdOn = datetime.utcnow()
        self.createdBy = get_current_identity()
        self.type = None
        self.status = "draft"
        self.comment = kwargs['comment']


    def get_details(self):
        return {
            "id":self.id,
            "createdOn": self.createdOn,
            "createdBy": self.createdBy,
            "type": self.type,
            "location": self.location,
            "status": self.status,
            "Images": self.Images,
            "Videos": self.Videos,
            "comment": self.comment,
        }


    def validate_location(self):
        location = str(self.location)
        error = None
        coordinates = self.location.split(' ')

        if not location or not isinstance(location,str):
            error = "Provide a location"
        elif not len(coordinates) == 2:
            error = "location must contain both latitude and longitude"
        return error

    def validate_comment(self):
        error = None

        if not self.comment:
            error = "Please provide a comment"
        elif not isinstance(self.comment, str):
            error = "Comment must be a string"
        return error


class RedFlag(Incident):
    flags_id =1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Red-flags"

    def add_red_flag(self):
        self.id =RedFlag.flags_id

        red_flags.append(self)
        RedFlag.flags_id += 1

red_flags = []
def check_if_red_flag_exists(red_flag_obj):
    for red_flag in red_flags:
        if red_flag.comment == red_flag_obj.comment and red_flag.location == red_flag_obj.location:
            return True
    return False


def get_all_record():
    records = []
    for redflag in red_flags:
        if redflag.createdBy == get_current_identity():
            records.append(redflag.get_details())
    return records

