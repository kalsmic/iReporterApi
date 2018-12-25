from datetime import datetime

red_flag_id = 1
red_flags = []
comment_id = 1
comments = []

time_now = datetime.now().strftime("%Y-%m-%d %H:%M")


class Incident:
    def __init__(self, title, description, **kwargs):
        self.title = title
        self.description = description
        self.tags = kwargs.get("tags", [])
        self.images = kwargs.get("images", [])
        self.videos = kwargs.get("videos", [])
        self.location = kwargs.get("location", {"Lat": "", "Long": ""})
        self.created_on = time_now
        self.created_by = kwargs.get("user_id")
        self.status = "draft"
        # self.comment = kwargs.get('comment')

    def get_details(self):
        return {
            "title": self.title,
            "description": self.description,
            "createdOn": self.created_on,
            "createdBy": self.created_by,
            "location": self.location,
            "status": self.status,
            "Images": self.images,
            "Videos": self.videos,
            "tags": self.tags,
        }


class RedFlag(Incident):
    def __init__(self, title, description, **kwargs):
        global red_flag_id
        self.incident_id = red_flag_id
        self.incident_type = "Red-flag"
        super().__init__(title, description, **kwargs)
        red_flag_id += 1

    def get_details(self):
        details = super().get_details()
        details["id"] = self.incident_id
        details["type"] = self.incident_type
        details["comments"] = get_incident_comments(self.incident_id)

        return details


class Comment:
    def __init__(self, incident_id, owner_id, body):
        global comment_id
        self.comment_id = comment_id
        self.incident_id = incident_id
        self.owner = owner_id
        self.body = body
        self.created_on = time_now
        comment_id += 1

    def get_details(self):
        return {
            "id": self.comment_id,
            "incidentId": self.incident_id,
            "commentBy": self.owner,
            "body": self.body,
            "createOn": self.created_on,
        }


records = {"red-flag": {"db": red_flags, "id": red_flag_id}}


def get_incident_record(record_id, collection):
    """Returns a redflag or Intervention record"""
    return [
        record.get_details() for record in collection if record.incident_id == record_id
    ]


def get_all_incident_records(collection):
    """ Parameter:Expects Intervention collection
        Returns: all red-flags if collection is red-flags else
        Returns: interventions if collection is interventions
    """
    return [record.get_details() for record in collection]


def get_incident_obj_by_id(incident_id, collection):
    return [record for record in collection if record.incident_id == incident_id]


def incident_record_exists(title, description, collection):
    return [
        record
        for record in collection
        if record.title == title and record.description == description
    ]


def get_comment_obj_by_id(comment_id, incident_id):
    return [
        comment_obj
        for comment_obj in comments
        if comment_obj.incident_id == incident_id
        and comment_obj.comment_id == comment_id
    ]


def get_incident_comments(incident_id):
    """Returns comments for a given incident record"""
    return [
        comment.get_details()
        for comment in comments
        if comment.incident_id == incident_id
    ]


def get_incident_comments(incident_id):
    """Returns comments for a given incident record"""
    return [
        comment.get_details()
        for comment in comments
        if comment.incident_id == incident_id
    ]
