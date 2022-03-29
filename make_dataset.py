import os
import natsort
import cv2
import numpy as np

def clean_files_list(files_list):
    cleaned_files = [f for f in files_list if not f.startswith('.')]
    return cleaned_files

def process_folder(folder_path, dest_dir):
    files = os.listdir(folder_path)
    cleaned_files = clean_files_list(files)
    sorted_clean_files = natsort.natsorted(cleaned_files)
    assert len(sorted_clean_files)>2, f"Not enough files in {folder_path}"
    sorted_clean_files.insert(0, None)
    
    # make a list of pairs like this:
    # [('0003a.jpg', '0003b.jpg'), ('0003b.jpg', '0003c.jpg')]
    filename_pairs = list(zip(sorted_clean_files, sorted_clean_files[1:]))[1:]

    for pair in filename_pairs:
        img_1_filename = os.path.join(folder_path, pair[0])
        img_2_filename = os.path.join(folder_path, pair[1])
        img_1 = cv2.imread(img_1_filename)
        img_2 = cv2.imread(img_2_filename)
        img_2 = cv2.resize(img_2, (img_1.shape[1], img_1.shape[0]))
        stacked_image = np.concatenate((img_1, img_2), axis=1)
        background_image = np.zeros((stacked_image.shape[0],stacked_image.shape[0]*2, 3), dtype=np.uint8)
        x_start = int(background_image.shape[1]/2) - int(stacked_image.shape[1]/2)
        background_image[0:stacked_image.shape[0], x_start:x_start+stacked_image.shape[1], :] = stacked_image
        sized_image = cv2.resize(background_image, (512, 256))
        # cv2.imshow("img1", img_1)
        # cv2.imshow("img2", img_2)
        # cv2.imshow("Combined", stacked_image)
        # cv2.imshow("Resized", sized_image)
        # cv2.imshow("Background", background_image)
        # cv2.waitKey(0)
        print(f"Stackedimg size: {stacked_image.shape}")
        print(f"Background size: {background_image.shape}")
        print(f"sized_img  size: {sized_image.shape}")
        image_destination = os.path.join(dest_dir, os.path.splitext(pair[0])[0]+"_and_"+os.path.splitext(pair[1])[0])+".jpg"
        print(f"writing {image_destination} ...")
        cv2.imwrite(image_destination, sized_image)



def process_root_dir(data_dir, dest_dir):
    folder_names = os.listdir(data_dir)
    clean_folder_names = clean_files_list(folder_names)
    folder_paths = [data_dir + p for p in clean_folder_names]

    for folder_path in folder_paths:
        process_folder(folder_path, dest_dir)



if __name__=="__main__":
    data_dir = "/Users/user/repos/gishe/data/from_gishe/"
    dest_dir = "/Users/user/repos/gishe/data/from_gishe_processed/"
    process_root_dir(data_dir, dest_dir)
