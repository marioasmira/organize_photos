import exiftool

files = ["test_rename/20211020_171551.mp4"]
with exiftool.ExifToolHelper() as et:
    metadata = et.get_metadata(files)
for d in metadata:
    print("{:20.40} {:20.20}".format(d["SourceFile"],
                                     d["QuickTime:CreateDate"]))

print(metadata[0]["QuickTime:CreateDate"][:4])