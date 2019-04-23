import io
import sys
import os
import json
import time
from dotenv import load_dotenv
from pymongo import MongoClient, TEXT, UpdateOne

mongoUri = os.getenv("DATA_TOOL_URI")
def progress(count, total, status=''):
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def readSegment(remaining, stream):
    data = []
    i = min((x for x in [remaining.find(b'\t'),remaining.find(b'\n')] if x > -1), default=-1)
    if i == -1:
        data.append(remaining)
    else:
        data.append(remaining[:i])
        data.append(b'\n')
        return b"".join(data), False, remaining[i+1:]
    while True:
        chunk = stream.read(512)
        if (chunk == b''):
            return b"".join(data), True, b''
        i = min((x for x in [chunk.find(b'\t'),chunk.find(b'\n')] if x > -1), default=-1)
        if i == -1:
            data.append(chunk)
        else:
            data.append(chunk[:i])
            break
    data.append(b'\n')
    return b"".join(data), False, chunk[i+1:]

def db_mod(data_type="EDITION"):
    load_dotenv(".env")
    client = MongoClient(mongoUri)
    db = client.book_db
    if data_type == "AUTHOR":
        db.authors.create_index([("name",TEXT)])
        db.authors.create_index("key")
    if data_type == "WORK":
        db.works.create_index([("title_cleaned",TEXT)])
        db.works.create_index("key")
    if data_type == "EDITION":
        db.editions.create_index([("title_cleaned",TEXT)])
        db.editions.create_index("key")
def upload(input, data_type="EDITION"):
    load_dotenv(".env")
    client = MongoClient(mongoUri)
    db = client.book_db;
    total_size = os.path.getsize(input)
    #max_upload_size = 1400
    #bulk_max_size = 1400;
    MAX_UPLOAD = False
    max_upload_size = 14000000
    bulk_max_size = 14000000;
    size_read = 0
    lastPrinted = 0
    bulk_count = 0;
    bulk_size = 0;
    bulk = []
    startTime = time.time();
    remaining = b''
    with open(input,'rb',buffering=256) as f:
        while True:
            seg, EOF, remaining = readSegment(remaining, f)
            seg_size = len(seg)
            size_read += seg_size
            try:
                seg_json = json.loads(seg.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                if EOF:
                    if data_type == "AUTHOR":
                        db.authors.insert_many(bulk)
                    if data_type == "WORK":
                        db.works.insert_many(bulk)
                    if data_type == "EDITION":
                        db.editions.insert_many(bulk)
                    break
                continue
            if data_type == "WORK" or data_type == "EDITION":
                if not 'title' in seg_json:
                    continue
            cleaned_title = seg_json["title"]
            cleaned_title = cleaned_title.replace(".","")
            cleaned_title = cleaned_title.replace(","," ")
            cleaned_title = cleaned_title.replace("'","")
            cleaned_title = cleaned_title.replace("?","")
            cleaned_title = cleaned_title.replace("/"," ")
            cleaned_title = cleaned_title.replace("\"","")
            cleaned_title = cleaned_title.replace("(","")
            cleaned_title = cleaned_title.replace(")","")
            seg_json["title_cleaned"] = cleaned_title
            if not 'authors' in seg_json:
                seg_json["authors"] = []
            if not 'subtitle' in seg_json:
                seg_json["subtitle"] = ""
            bulk.append(UpdateOne({"title":{"$regex":"/^"+seg_json["title"]+"$/i"},"subtitle":{"$regex":"/^"+seg_json["subtitle"]+"$/i"},"authors":seg_json["authors"]},seg_json, upsert=True))
            bulk_size += seg_size
            bulk_count += 1
            if MAX_UPLOAD:
                if size_read > max_upload_size:
                    if data_type == "AUTHOR":
                        db.authors.insert_many(bulk)
                    if data_type == "WORK":
                        db.works.insert_many(bulk)
                    if data_type == "EDITION":
                        db.editions.insert_many(bulk)
                    break

            if bulk_size > bulk_max_size:
                bulk_count = 0
                if data_type == "AUTHOR":
                    db.authors.insert_many(bulk)
                if data_type == "WORK":
                    db.works.insert_many(bulk)
                if data_type == "EDITION":
                    db.editions.insert_many(bulk)
                bulk = []
                bulk_size = 0

            currentPercent = size_read/total_size
            if currentPercent-lastPrinted > 0.001:
                progress(size_read,total_size, "UPLOADED")
                lastPrinted = currentPercent
            if EOF:
                if data_type == "AUTHOR":
                    db.authors.insert_many(bulk)
                if data_type == "WORK":
                    db.works.insert_many(bulk)
                if data_type == "EDITION":
                    db.editions.insert_many(bulk)
                break

    endTime = time.time()
    elapsed = endTime - startTime
    print()
    print("Elapsed Seconds:")
    print(elapsed)
def clean(input, output, data_type="EDITION"):
    author_elements = ["name", "personal_name", "birth_date","death_date", "key"]
    edition_elements = ["title","subtitle","key","isbn_10","isbn_13","number_of_pages","publish_date","authors","subjects"]
    work_elements = ["title","key","authors"]
    total_size = os.path.getsize(input)
    size_read = 0
    lastPrinted = 0
    startTime = time.time();
    remaining = b''
    with open(input,'rb',buffering=1024) as f:
        while True:
            for i in range(0,5):
                seg, EOF, remaining = readSegment(remaining, f)
                seg_size = len(seg)
                size_read += seg_size
            try:
                seg_json = json.loads(seg.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                if EOF:
                    break
                continue

            for element in list(seg_json.keys()):
                if element not in work_elements:
                    seg_json.pop(element, None)
                if data_type == "AUTHOR":
                    if element == "name":
                        if len(seg_json[element]) >= 50:
                            seg_json[element] = seg_json[element][:50]

            currentPercent = size_read/total_size
            if currentPercent-lastPrinted > 0.001:
                progress(size_read,total_size, "CLEANED")
                lastPrinted = currentPercent


            with open(output, "a") as writeFile:
                json.dump(seg_json,writeFile)
                writeFile.write("\n")
            if EOF:
                break
    endTime = time.time()
    elapsed = endTime - startTime
    print()
    print("Elapsed Seconds:")
    print(elapsed)
if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Bad Arguements")
        exit()
    run_mode = sys.argv[1]
    data_mode = sys.argv[2]
    if not data_mode == "EDITION" and not data_mode == "WORK" and not data_mode == "AUTHOR":
        print("Incorrect Data Type")

    inputFile = "A:/editions.txt"
    outputFile = "A:/editions_cleaned.txt"
    if run_mode == "CLEAN":
        clean(inputFile, outputFile, data_type=data_mode)
    if run_mode == "UPLOAD":
        upload(inputFile, data_type=data_mode)
    if run_mode == "MOD":
        db_mod(data_type=data_mode)
