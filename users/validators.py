def validate_create_post(text=None, image=None):
    if not text and not image:
        return {"status": False, "text": "Invalid form"}
    if image:
        if str(image)[int(str(image).rfind(".")):] not in [".png", ".jpeg", ".jpg", ".webp"]:
            return {"status": False, "text": "The format of file isn't support"}
        elif image.size > 2 * 1024 * 1024:
            return {"status": False, "text": "File is too big"}
    if text:
        if len(text) > 600:
            return {"status": False, "text": "Text is too big"}
    return {"status": True, "text": "You created post successfully"}