import os
import time

# 다운로드 폴더에 pptx 파일이 생성될 때까지 대기
def wait_for_download(download_dir, expected_ext=None, timeout=60):
    end_time = time.time() + timeout

    # timeout 까지 반복 확인
    while time.time() < end_time:
        # 다운로드 폴더 내 모든 파일 목록 조회
        files = os.listdir(download_dir)

        if expected_ext:
            # 특정 확장자 파일만 필터링
            # (다운로드 중인 .crdownload, .tmp 파일 제외)
            files = [
                f for f in files
                if f.endswith(expected_ext) and not f.endswith(".crdownload") and not f.endswith(".tmp")
            ]
        else:
            files = [
                f for f in files
                if not f.endswith(".crdownload") and not f.endswith(".tmp")
            ]

        # 조건에 맞는 파일이 있으면 반환
        if files:
            return files[0]

        time.sleep(1)

    raise TimeoutError(f"{expected_ext} 파일 다운로드 시간 초과")

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

