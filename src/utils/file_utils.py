import os
import time

# 다운로드 폴더에 pptx 파일이 생성될 때까지 대기
def wait_for_download(download_dir, timeout=60):
    end_time = time.time() + timeout

    while time.time() < end_time:
        files = [
            f for f in os.listdir(download_dir)
            if f.endswith(".pptx")
        ]

        if files:
            return files[0]

        time.sleep(1)

    raise TimeoutError("PPTX 파일 다운로드 시간 초과")

# 다운로드 폴더 초기화
def clean_download_dir(download_dir):
    """
    다운로드 폴더 초기화
    - 이전 테스트 잔여 파일 제거
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        return

    for f in os.listdir(download_dir):
        try:
            os.remove(os.path.join(download_dir, f))
        except Exception as e:
            print(f"[WARN] 파일 삭제 실패: {f} ({e})")

