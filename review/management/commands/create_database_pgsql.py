from django.core.management.base import BaseCommand
from django.conf import settings
import json
import uuid
import psycopg2
from django.utils import timezone



class Command(BaseCommand):
    help = 'Create Database'

    def handle(self, *args, **options):
        conn = psycopg2.connect("postgres://tsukureview:0EcsTAiiPKaC3TSGTe2jRhyuiI82h7Qf@dpg-cdt0a2ien0hlde2jdsng-a/tsukureview_beta_db")
        cur = conn.cursor()

        with open("kdb.json", "r", encoding="utf-8") as f:
            kdb = json.load(f)

        print("講義データベース・スレッド生成プログラム")
        print(f"kdb.json Updated at {kdb['updated']}")

        print("スレッド生成を開始します。")

        for sub in kdb["subject"]:
            msg_sender_name = "システム"
            msg_title = "この投稿はシステムメッセージです。"
            msg_overall = "記入例) とても面白かった。"
            msg_difficulty = "記入例) とても簡単だった。"
            msg_kadai = "記入例) とても少なかった。"
            msg_evaluation = "記入例) とても甘かった。"
            review_id = str(uuid.uuid4()).replace("-", "")
            year = 2022
            rating = 5
            grade = 5
            review = [sub[0], review_id, msg_sender_name, 1, msg_title, year,
                    rating, grade, msg_overall, msg_difficulty, msg_kadai, msg_evaluation, timezone.now()]
            col = [sub[0], sub[1], sub[3], sub[4], sub[5], sub[8],
                sub[9], sub[13], sub[14], sub[15]]
            cur.execute("insert into review_subject("
                        + "code,name,unit,grade,semester,teachers,overview,subtype,schools,colleges"
                        + ") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", col)
            cur.execute("insert into review_review("
                        + "lecture_id,review_id,sender_name,sender_college,title,year,rating,grade,overall,difficulty,kadai,evaluation,created_at"
                        + ") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", review)

        print("スレッド生成が完了しました。")
        conn.commit()
        conn.close()
