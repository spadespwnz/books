import io
import sys
import os
import json
import time
from dotenv import load_dotenv
from pymongo import MongoClient
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

def db_mod():
    load_dotenv(".env")
    mongoUri = os.getenv("MONGO_DB_URI")
    client = MongoClient(mongoUri)
    db = client.get_default_database()
    db.authors.create_index("name")
    db.authors.create_index("key")
def upload(input):
    load_dotenv(".env")
    mongoUri = os.getenv("MONGO_DB_URI")
    client = MongoClient(mongoUri)
    db = client.get_default_database()
    total_size = os.path.getsize(input)
    max_upload_size = 14000000*5
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
                    db.authors.insert_many(bulk)
                    break
                continue
            bulk.append(seg_json)
            bulk_size += seg_size
            bulk_count += 1
            if size_read > max_upload_size:
                db.authors.insert_many(bulk)
                break

            if bulk_size > bulk_max_size:
                bulk_count = 0
                db.authors.insert_many(bulk)
                bulk = []
                bulk_size = 0

            currentPercent = size_read/total_size
            if currentPercent-lastPrinted > 0.001:
                progress(size_read,total_size, "CLEANED")
                lastPrinted = currentPercent
            if EOF:
                db.authors.insert_many(bulk)
                break

    endTime = time.time()
    elapsed = endTime - startTime
    print()
    print("Elapsed Seconds:")
    print(elapsed)
def clean(input, output, data_type="AUTHOR"):
    author_elements = ["name", "personal_name", "birth_date","death_date", "key"]
    edition_elements = ["title","subtitle","key","isbn_10","isbn_13","number_of_pages","publish_date","authors","subjects"]
    work_elements = ["title","key","author","authors"]
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
                if element not in author_elements:
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
    if len(sys.argv) <= 1:
        exit()
    run_mode = sys.argv[1]

    inputFile = "A:/authors_cleaned.txt"
    outputFile = "A:/authors_cleaned.txt"
    if run_mode == "CLEAN":
        clean(inputFile, outputFile)
    if run_mode == "UPLOAD":
        upload(inputFile)
    if run_mode == "MOD":
        db_mod()
