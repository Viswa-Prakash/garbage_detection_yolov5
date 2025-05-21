import os,sys
import yaml
from garbage.utils.main_utils import read_yaml_file
from six.moves import urllib
from garbage.logger import logging
from garbage.exception import GDException
from garbage.constant.training_pipeline import *
from garbage.entity.config_entity import ModelTrainerConfig
from garbage.entity.artifacts_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config

    
    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try: 
            logging.info("Unzipping data")
            os.system(f"unzip {DATA_INGESTION_S3_DATA_NAME}")
            os.system(f"rm {DATA_INGESTION_S3_DATA_NAME}")

            #Prepare image path in txt file
            train_img_path = os.path.join(os.getcwd(),"images","train")
            val_img_path = os.path.join(os.getcwd(),"images","val")

            #Training images
            with open('train.txt', "a+") as f:
                img_list = os.listdir(train_img_path)
                for img in img_list:
                    f.write(os.path.join(train_img_path,img+'\n'))
                print("Done Training images")


            # Validation Image
            with open('val.txt', "a+") as f:
                img_list = os.listdir(val_img_path)
                for img in img_list:
                    f.write(os.path.join(val_img_path,img+'\n'))
                print("Done Validation Image")


            
            # download COCO starting checkpoint
            url = self.model_trainer_config.weight_name
            file_name = os.path.basename(url)
            urllib.request.urlretrieve(url, os.path.join("yolov5", file_name))


            #training
            os.system(f"cd yolov5 && python train.py --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_epochs} --data data/custom.yaml --weights yolov5s.pt")

            os.system("cp yolov5/runs/train/exp/weights/best.pt yolov5/")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            os.system(f"cp yolov5/runs/train/exp/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")

            os.system("rm -rf yolov5/runs")
            os.system("rm -rf images")
            os.system("rm -rf labels")
            os.system("rm -rf classes.names")
            os.system("rm -rf train.txt")
            os.system("rm -rf val.txt")
            os.system("rm -rf train.cache")
            os.system("rm -rf val.cache")


            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact


        except Exception as e:
            raise GDException(e, sys)