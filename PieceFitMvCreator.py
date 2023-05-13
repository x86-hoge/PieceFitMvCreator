import cv2
import time

class PieceFitMvCreator:
    def __init__(self, background_img_path, overlap_img_path, overlay_img_path, fixed_img_path, duration_sec, slide_distance): 
        self.base_size = (400,600)
        self.slider_size = (64,64)
        self.background_img = cv2.resize(cv2.imread(background_img_path), self.base_size)
        self.overlap_img = cv2.resize(cv2.imread(overlap_img_path), self.base_size)
        self.overlay_img = cv2.resize(cv2.imread(overlay_img_path), self.slider_size)
        self.base_cut_flg = False
        self.fixed_img = cv2.resize(cv2.imread(fixed_img_path), self.slider_size)
        self.output_file_path = str(time.time()).replace('.','')+'_out.mp4'
        self.duration_sec = duration_sec
        self.slide_distance = slide_distance
        self.fps = 30
        
    def run(self):
        try:
            
            arr =[]
            base = self.background_img.copy()

            base_height, base_width, _ = base.shape
            fixed_height, fixed_width, _ = self.fixed_img.shape
            overlap_img_height, overlap_img_width, _ = self.overlap_img.shape
            fit_pos_x = 150
            fix_pos_y = self.base_size[1]-200-fixed_height

            if self.base_cut_flg:
                self.overlay_img = base.copy()
                self.overlay_img = self.overlay_img[fix_pos_y:fix_pos_y+self.slider_size[1], fit_pos_x:fit_pos_x+self.slider_size[0]]

            overlay_img_height, overlay_img_width,_ = self.overlay_img.shape
            
            base[fix_pos_y:fix_pos_y+fixed_height, fit_pos_x:fit_pos_x+fixed_width] = self.fixed_img
            
            x_position = -overlay_img_width

            for _ in range(int(self.duration_sec * self.fps)):
                img = base.copy()

                #screen fade in
                if 0 > x_position:
                    diff_width = x_position+overlay_img_width
                    img[fix_pos_y:fix_pos_y+overlay_img_height, base_width-diff_width:base_width] = self.overlay_img[0:overlay_img_height, 0:diff_width]
                
                #screen fade out
                elif x_position+overlay_img_width > base_width:
                    diff_width = x_position+overlay_img_width-base_width
                    img[fix_pos_y:fix_pos_y+overlay_img_height, 0:overlay_img_width-diff_width] = self.overlay_img[0:overlay_img_height, diff_width:overlay_img_width]
                
                #screen range
                else:
                    img[fix_pos_y:fix_pos_y+overlay_img_height, base_width-overlay_img_width-x_position:base_width-x_position] = self.overlay_img
                    if x_position <= base_width-fit_pos_x-overlay_img_height and x_position > base_width-fit_pos_x-overlay_img_height-3:
                        img[0:overlap_img_height, 0:overlap_img_width] = self.overlap_img

                arr.append(img)
                x_position += self.slide_distance
                
                if x_position > base_width:
                    x_position = -overlay_img_width
 
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(self.output_file_path, fourcc, self.fps,self.base_size)

            for i in arr:
                video_writer.write(i)

            video_writer.release()

        except Exception as e:
            print(e)