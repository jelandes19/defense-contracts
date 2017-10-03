import download_util

drive_id = "0B-OkbOhjvGmXN0Q0QUVfZjE2TUU"
zip_file_name = "dod_raw_html.zip"

def main():
    download_util.download_file_from_google_drive(drive_id, zip_file_name)

if __name__ == "__main__":
    main()
