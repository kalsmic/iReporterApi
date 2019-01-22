from database.db import Database


class Incident:
    def __init__(self):
        self.db = Database()

    def insert_incident(self, inc_type="red-flag", **kwargs):
        title = kwargs.get("title")
        comment = kwargs.get("comment")
        location = (kwargs.get("location")[0], kwargs.get("location")[1])
        created_by = kwargs.get("user_id")
        images = kwargs.get("images")
        videos = kwargs.get("videos")
        sql = (
            "INSERT INTO public.incidents ("
            "title, comment, location, created_by, type"
            ")VALUES ("
            f"'{title}', '{comment}','{location}',"
            f"'{created_by}', '{inc_type}') returning id;"
        )
        self.db.cursor.execute(sql)
        last_insert_id = self.db.cursor.fetchone()
        new_incident_id = last_insert_id.get("id")
        self.insert_images(new_incident_id, images)
        self.insert_videos(new_incident_id, videos)
        return self.get_incident_by_id(inc_type, new_incident_id)

    def insert_images(self, incident_id, images):
        for image in images:
            sql = (
                "INSERT INTO public.incident_images ("
                "incident_id,image_url) VALUES ("
                f"'{incident_id}','{image}');"
            )
            self.db.cursor.execute(sql)

    def insert_videos(self, incident_id, videos):
        for video in videos:
            sql = (
                "INSERT INTO public.incident_videos ("
                "incident_id,video_url) VALUES ("
                f"'{incident_id}','{video}');"
            )
            self.db.cursor.execute(sql)

    def get_incident_by_id(self, inc_type, inc_id):

        sql = (
            f"SELECT * FROM public.incident_view "
            f"WHERE id='{inc_id}' AND type='{inc_type}';"
        )
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()

    def incident_record_exists(self, title, comment):
        sql = (
            "SELECT count(*) FROM incidents WHERE "
            f"title='{title}' AND comment='{comment}';"
        )
        self.db.cursor.execute(sql)
        duplicates = self.db.cursor.fetchone()
        if duplicates["count"]:
            return True
        return False

