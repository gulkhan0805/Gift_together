import cloudinary
import cloudinary.uploader

cloudinary.config( 
  cloud_name = "di80pp52x", 
  api_key = "997571313277177", 
  api_secret = "sLXRm-HIF1TH-OXSyqG3-TwxZWs"
)

UPLOAD_PRESET = "wedding_preset"  # Change this to your actual unsigned preset name if different

def upload_image(file):
      try:
        result = cloudinary.uploader.upload(
            file,
            folder="wedding_gifts/",  # optional
        )
        return result["secure_url"]
    except Exception as e:
        print("Cloudinary upload failed:", e)
        return No