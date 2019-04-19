import io
import sys
import os
import json
def readSegment(stream):
    data = []
    while True:
        chunk = stream.read(1)
        if (chunk == b''):
            return b"".join(data), True
        i = chunk.find(b'\t') + chunk.find(b'\n')
        if i == -2:
            data.append(chunk)
        else:
            break
    data.append(b'\n')
    return b"".join(data), False


if __name__ == "__main__":
    author_elements = ["name", "personal_name", "birth_date","death_date", "key"]
    total_size = os.path.getsize('test1.txt')
    size_read = 0
    with open("test1.txt",'rb',buffering=256) as f:
        while True:
            for i in range(0,5):
                seg, EOF = readSegment(f)
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

            print(str(size_read/total_size))

            with open("test2.txt", "a") as writeFile:
                json.dump(seg_json,writeFile)
                writeFile.write("\n")
            if EOF:
                break
