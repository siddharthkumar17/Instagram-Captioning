from nn_captioner import Caption
from scrapeIG import Scraper
from build_vocab import Vocabulary
import argparse
from skimage import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def displayImages(imgs,captions, output_path):
    images = []
    for img_path in imgs:
        images.append(mpimg.imread(img_path))
        
#     plt.figure(figsize=(20,10))
#     columns = 4
#     for i, image in enumerate(images):
#         plt.subplot(len(images) / columns + 1, columns, i + 1)
#         plt.imshow(image)
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(40, 30), subplot_kw={'xticks': [], 'yticks': []})
    x=0
    for ax, img in zip(axs.flat, images):
        ax.imshow(img)
        ax.set_title(captions[imgs[x]], fontsize=25)
        x+=1
    plt.tight_layout()
    plt.savefig(output_path)
    
    

def main(args):
    
    USER_NAME = args.user_name

    captioner = Caption()
    s = Scraper(user_name=USER_NAME)

    image_src = s.scrape()

    image_paths = s.getImagesFromSource(image_src)

    captions = captioner.getCaption(image_paths, output_path=args.output_path)

    
    displayImages(image_paths, captions, args.output_path)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--user_name', type=str, required=False, default='photos', help = 'user name to caption')
    parser.add_argument('--output_path', type=str, required=False, default='captions.png', help = 'path for output file')
    
    args = parser.parse_args()
    main(args)