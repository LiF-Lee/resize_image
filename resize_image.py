from PIL import Image, ImageFile
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_image_format(extension):
    extension = extension.lower()
    if extension in [".jpg", ".jpeg"]:
        return "JPEG"
    elif extension == ".png":
        return "PNG"
    elif extension == ".gif":
        return "GIF"
    elif extension == ".bmp":
        return "BMP"
    elif extension == ".tiff":
        return "TIFF"
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {extension}")

def resize_images(source_folder, target_folder, width, height, save_original_ext, save_format=None):
    target_size = (width, height)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    failed_images = []

    for filename in os.listdir(source_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".ico", ".webp")):
            try:
                img_path = os.path.join(source_folder, filename)
                img = Image.open(img_path)
                img_resized = img.resize(target_size)
                
                if img_resized.mode == "RGBA" and save_format.lower() in ["jpg", "jpeg"]:
                    img_resized = img_resized.convert("RGB")

                base_filename, original_ext = os.path.splitext(filename)
                
                if save_original_ext:
                    target_filename = f"{base_filename}{original_ext}"
                    format = get_image_format(original_ext)
                else:
                    target_filename = f"{base_filename}.{save_format.lower()}"
                    format = get_image_format(f".{save_format}")
                
                target_path = os.path.join(target_folder, target_filename)
                img_resized.save(target_path, format=format)
                print(f"{filename} -> {target_filename} 사이즈 변환 완료")
            except Exception as e:
                print(f"{filename} 사이즈 변환 실패: {e}")
                failed_images.append(filename)

    if failed_images:
        print("\n변환에 실패한 이미지 목록:")
        for failed_image in failed_images:
            print(failed_image)

try:
    source_folder = input("폴더 경로를 입력하세요. (예시: C:\\Users\\Downloads\\2024)\n=> ")
    width = int(input("\n변환할 이미지의 너비를 입력하세요. (예시: 315)\n=> "))
    height = int(input("\n변환할 이미지의 높이를 입력하세요. (예시: 420)\n=> "))
    
    keep_original = input("\n원본 확장자를 유지하시겠습니까? (y/n)\n=> ").lower() == "y"
    save_format = None
    if not keep_original:
        save_format = input("\n저장할 이미지 확장자 입력하세요. (예시: jpg, png)\n=> ")
    
    print()
    
    target_folder = source_folder + "_resized"

    resize_images(source_folder, target_folder, width, height, keep_original, save_format)

    input("\n작업이 완료되었습니다. 창을 닫으려면 아무 키나 누르세요...")
except ValueError as e:
    print(e)
except Exception as e:
    print(f"오류 발생: {e}")
