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

    # def upload_video(self,**Kwargs):

    #
    # def __repr__(self):
    #     return f"""{
    #         location:{self.locaiton},
    #         Images:{self.Images},
    #         Videos:{self.Videos},
    #         comment:{self.comment}
    #     }"""


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


    # description:{self.description},
#
#
#
#     def get_details(self):
#         return {
#             "location":{"latitute":self.}
#         }
#
#     def get_location(self):
#         return {
#             "latitute":self.location['latitude'],
#             "longitude":self.location['longitude']
#         }
#
#
#
# #     def validata_input_data(self):
# #         """validates input data"""
# #         error = None
#
# #         if not self.location['latitude'] or not self.location['longitude']:
# #             error = "latitude and longitude must be present in location"
#
# #         elif not self.description or not isinstance(self.description, str):
# #             error = "provide a valid description"
# #         elif len(self.Images):
# #             """verify image type"""
# #             for image in self.Images:
# #                 if not ".jpg" in image:
# #                     error = "Only Images with .jpg extension are supported"
# #                     break
#
# #         elif len(self.Videos):
# #             for video in self.Videos:
# #                 if not "mp4" in video:
# #                     error = "Only Videos with .mp4 extension are supported"
# #                     break
# #         elif not self.comment:
# #             error = "Please add a comment"
# #         return error
#
# # class RedFlag(Incident):
#
# #     def __init__(self,**kwargs):
# #         super.__init__(self,**kwargs)
# #         self.type = "Red-flag"
#
# # class Intervention(Incident):
#
# #     def __init__(self,**kwargs):
# #         super.__init__(self,**kwargs)
# #         self.type = "Intervention"
#
#
# # if __name__ == "__main__":
# #     inc1 = Incident(
# #         location={"latitude": 14.3362, "longitude": 67.4433},
# #         description="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
# #         Images=["image1.jpg"], Videos=["video1.mp4", "video2.mp4"], comment="Needs urgent action")
# #     print(inc1.validata_input_data())
#
