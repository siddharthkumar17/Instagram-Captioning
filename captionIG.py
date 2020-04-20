from nn_captioner import Caption
from scrapeIG import Scraper
from build_vocab import Vocabulary
import argparse


def main(args):
    
    USER_NAME = args.user_name

    captioner = Caption()
    s = Scraper(user_name=USER_NAME)

    image_src = s.scrape()

    image_paths = s.getImagesFromSource(image_src)

    captions = captioner.getCaption(image_paths, output_path=args.output_path)

    print(captions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--user_name', type=str, required=False, default='photos', help = 'user name to caption')
    parser.add_argument('--output_path', type=str, required=False, default='', help = 'path for output file')

    args = parser.parse_args()
    main(args)