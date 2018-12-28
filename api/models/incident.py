from datetime import datetime

red_flag_id = 1
red_flags = []

time_now = datetime.now().strftime("%Y-%m-%d %H:%M")


class Incident:
    def __init__(self, title, comment, **kwargs):
        self.title = title
        self.comment = comment
        self.tags = kwargs.get("tags", [])
        self.images = kwargs.get("images", [])
        self.videos = kwargs.get("videos", [])
        self.location = kwargs.get("location", {"Lat": "", "Long": ""})
        self.created_on = time_now
        self.created_by = kwargs.get("user_id")
        self.status = "draft"

    def get_details(self):
        return {
            "title": self.title,
            "comment": self.comment,
            "createdOn": self.created_on,
            "createdBy": self.created_by,
            "location": self.location,
            "status": self.status,
            "Images": self.images,
            "Videos": self.videos,
            "tags": self.tags,
        }


class RedFlag(Incident):
    def __init__(self, title, comment, **kwargs):
        global red_flag_id
        self.incident_id = red_flag_id
        self.incident_type = "Red-flag"
        super().__init__(title, comment, **kwargs)
        red_flag_id += 1

    def get_details(self):
        details = super().get_details()
        details["id"] = self.incident_id
        details["type"] = self.incident_type

        return details


records = {"red-flag": {"db": red_flags, "id": red_flag_id}}


def get_incident_record(record_id, collection):
    """Returns a redflag or Intervention record"""
    return [
        record.get_details()
        for record in collection
        if record.incident_id == record_id
    ]


def get_all_incident_records(collection):
    """ Parameter:Expects Intervention collection
        Returns: all red-flags if collection is red-flags else
        Returns: interventions if collection is interventions
    """
    return [record.get_details() for record in collection]


def get_incident_obj_by_id(incident_id, collection):
    for record in collection:
        if record.incident_id == incident_id:
            return record
    return None


def incident_record_exists(title, comment, incident_results):
    for incident_result in incident_results:
        if (
            incident_result.title == title
            and incident_result.comment == comment
        ):
            return True
    return False
