import sys,os
from garbage.pipeline.training_pipeline import TrainPipeline
from garbage.logger import logging
from garbage.exception import GDException
from garbage.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template,Response
from flask_cors import CORS, cross_origin
from garbage.configuration.s3_operations import S3Operation
from garbage.entity.config_entity import ModelPusherConfig
import pathlib
pathlib.PosixPath = pathlib.WindowsPath
import glob


# initialize flask app
app = Flask(__name__)
CORS(app)

# user provided image
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"



@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return 
    

# render home page
@app.route("/")
def home():
    return render_template("index.html")

# After training, best.pt is saved in yolov5 dir locally, since yolov5 is cloned, it wont be pushed to github  
# Hence best.pt wont be available for prediction after app deployment in cloud. So we need to get best.pt weights from s3 bucket

def download_weights_from_s3():
    """
    Fetch best.pt weights from S3
    """
    try:
        # getting model name from model pusher config
        model_pusher_config = ModelPusherConfig()
        s3 = S3Operation()

        # destination dir for saving weights
        destination_dir = 'yolov5' + "/" + model_pusher_config.S3_MODEL_KEY_PATH # yolov5/best.pt
        
        # check for weights availability locally or else download from S3 
        if os.path.exists(destination_dir):
            logging.info(f"Model file already exist: {destination_dir}")


        else:
            s3.download_object(key = model_pusher_config.S3_MODEL_KEY_PATH,
                               bucket_name = model_pusher_config.MODEL_BUCKET_NAME,
                               filename = destination_dir)
            
            logging.info(f"Weights are successfully downloaded from S3 Bucket: {model_pusher_config.MODEL_BUCKET_NAME}/{model_pusher_config.S3_MODEL_KEY_PATH}")
    
        return model_pusher_config.S3_MODEL_KEY_PATH


    except Exception as e:
        raise GDException (e,sys) from e
 


@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)

        weight_file = download_weights_from_s3()
        os.system("cd yolov5/ && python detect.py --weights best.pt  --source ../data/inputImage.jpg")

        # Get the latest saved image
        exp_dir = "yolov5/runs/detect/exp"
        image_path_list = glob.glob(os.path.join(exp_dir, "*.jpg"))
        if image_path_list:
            output_img_path = image_path_list[0]  # assumes only one image
            opencodedbase64 = encodeImageIntoBase64(output_img_path)
        else:
            raise FileNotFoundError("No image found in detection output folder.")

        result = {"image": opencodedbase64.decode('utf-8')}
        os.system("rm -rf yolov5/runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)


if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=8080, debug=True)
    