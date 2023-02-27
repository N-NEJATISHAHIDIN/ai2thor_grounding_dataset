import numpy as np
import argparse
import os
import sys
import cv2




# ai2thore 
import ai2thor
import ai2thor.util
from ai2thor.controller import Controller





def main(args):

    # Start a new scene with a specified scene name
    controller = Controller(
        agentMode="default",
        visibilityDistance=1.5,
        scene= args.scene_name,

        # step sizes
        gridSize=0.5,
        snapToGrid=True,
        rotateStepDegrees=90,



        # camera properties
        width=800,
        height=800,
        fieldOfView=90
    )
    event = controller.step(action='Initialize',
                                    
                            # image modalities
                            renderDepthImage = args.renderMidLevelImgs,
                            renderInstanceSegmentation = args.renderMidLevelImgs,
                            renderSemanticSegmentation = args.renderMidLevelImgs,
                            renderNormalsImage = args.renderMidLevelImgs
                            )




    #generate direcories to save images
    if args.renderMidLevelImgs :
        directory_renderRGBImage = args.d+"/renderedRGBImage"
        directory_renderDepthImage = args.d+"/enderedDepthImage"
        directory_renderInstanceSegmentation = args.d+"/renderedInstanceSegmentation"
        directory_renderSemanticSegmentation = args.d+"/renderedSemanticSegmentation"
        directory_renderNormalsImage = args.d+"/renderedNormalsImage"

    directories = [directory_renderRGBImage, directory_renderDepthImage, directory_renderInstanceSegmentation, 
                    directory_renderSemanticSegmentation, directory_renderNormalsImage]
    frame_names = ["frame", "depth_frame","instance_segmentation_frame", "semantic_segmentation_frame", "normals_frame"] #, "instance_detections2D", ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
    



    for i in range(10):
        event = controller.step(action='MoveRight')
        img_name = "img_"+ str(i)+".png"

        #camera_info 
        # print('agent:', event.metadata['agent'])
        # print('objects 3D bounding box on image:' , event.metadata['objects'][0]["axisAlignedBoundingBox"])
        # print('objects 3D bounding box on scene:' , event.metadata['objects'][0]["objectOrientedBoundingBox"])

        #event.metadata['objects'][0]["objectOrientedBoundingBox"]
        import pdb; pdb.set_trace()


        for index, directory in enumerate(directories): 
            print(os.path.join(directory,img_name))
            cv2.imwrite(os.path.join(directory,img_name), getattr(event,frame_names[index]))





if __name__ == '__main__':

    # Create the parser
    parser = argparse.ArgumentParser(prog = 'generate_dataset', 
                                     description = 'Generate Synthetic Images for 3D Vision and language special relationships')

    # Add an argument
    parser.add_argument('--d', '--dataset_directory', type= str, default='synthetic_ai2thor_data', help='the name of the scene to generate data from.')
    parser.add_argument('--scene_name', type= str, default='FloorPlan212', help='the name of the scene to generate data from.')
    parser.add_argument('--renderMidLevelImgs', action='store_true', default=True, help='Set the flag to false if not renderRGB ')


    # Parse the arguments
    args = parser.parse_args()

    main(args)