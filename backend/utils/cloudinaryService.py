from dotenv import load_dotenv

load_dotenv()
import cloudinary
import cloudinary.api
import cloudinary.uploader

cloudinary.config(secure=True)


def uploadMedia(file, public_id):
    try:
        res = cloudinary.uploader.upload(
            file=file,
            public_id=public_id,
            overwrite=True,
            resource_type="auto",
        )
        return res
    except Exception as e:
        print(f"Error uploading media: {e}")
        raise Exception(e)


def deleteMedia(public_id: list[str]):
    try:
        res = cloudinary.api.delete_resources(public_ids=public_id)
        return res
    except Exception as e:
        print(f"Error deleting media: {e}")
        raise Exception(e)
