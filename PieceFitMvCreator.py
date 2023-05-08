import cv2
import time

class PieceFitMvCreator:
    def __init__(self, background_img_path, overlap_img_path, overlay_img_path, duration_sec, slide_distance): 
        self.base_size = (400,600)
        self.background_img = cv2.resize(cv2.imread(background_img_path), self.base_size)
        self.overlap_img = cv2.resize(cv2.imread(overlap_img_path), self.base_size)
        self.overlay_img = cv2.resize(cv2.imread(overlay_img_path), (64,64))
        self.fixed_img = cv2.resize(cv2.imread(overlay_img_path), (64,64))
        self.output_file_path = str(time.time()).replace('.','')+'_out.mp4'
        self.duration_sec = duration_sec
        self.slide_distance = slide_distance
        self.fps = 30.0
        
    def run(self):
        try:
            x_position = 0
            arr =[]
            base = self.background_img.copy()
            
            fixed_img_height, fixed_img_width, _ = (self.fixed_img.shape)
            cmn_height = self.base_size[1]-40-fixed_img_height
            base[cmn_height:cmn_height+fixed_img_height, 100:100+fixed_img_width] = self.fixed_img
            for _ in range(int(self.duration_sec * self.fps)):
                img = base.copy()
                
                overlay_img_height, overlay_img_width, _ = self.overlay_img.shape
                img[cmn_height:cmn_height+overlay_img_height, self.base_size[0]-overlay_img_width-x_position:self.base_size[0]-x_position] = self.overlay_img

                if x_position <= 200 and x_position > 200-2:
                    overlap_img_height, overlap_img_width, _ = self.overlap_img.shape
                    img[0:overlap_img_height, 0:overlap_img_width] = self.overlap_img
                arr.append(img)

                x_position += self.slide_distance
                if x_position >= self.background_img.shape[0]:
                    x_position = 0

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(self.output_file_path, fourcc, self.fps,self.base_size)
            for i in arr:
                video_writer.write(i)

            video_writer.release()

        except Exception as e:
            print(e)