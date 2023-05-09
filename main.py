from PieceFitMvCreator import PieceFitMvCreator

background_img_path = 'background.png'
overlay_img_path = 'piece.png'
overlap_img_path = 'overlap.png'
duration_sec =25
slide_distance = 3

if __name__ == "__main__":
    pfmc = PieceFitMvCreator(
        background_img_path,
        overlap_img_path,
        overlay_img_path,
        duration_sec,
        slide_distance)
    pfmc.run()