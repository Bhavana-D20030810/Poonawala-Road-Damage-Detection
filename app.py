"""Upload an image to view detected road defects and a transparent severity proxy."""
import os
from pathlib import Path
import gradio as gr
from PIL import Image,ImageDraw,ImageFont
from ultralytics import YOLO

WEIGHTS=Path(os.getenv('ROAD_MODEL','models/best.pt'))
if not WEIGHTS.is_file():
    raise FileNotFoundError(f'Missing trained weights: {WEIGHTS}. Place best.pt in models/.')
MODEL=YOLO(str(WEIGHTS))

def severity_proxy(box_area,image_area):
    ratio=box_area/image_area
    return ('Low' if ratio<.01 else 'Medium' if ratio<.04 else 'High'),ratio

def inspect(image,confidence):
    if image is None:return None,[], 'Upload a road image.'
    image=image.convert('RGB')
    result=MODEL.predict(image,conf=confidence,verbose=False)[0]
    annotated=image.copy();draw=ImageDraw.Draw(annotated)
    rows=[];w,h=image.size
    for box in result.boxes:
        x1,y1,x2,y2=[float(v) for v in box.xyxy[0].tolist()]
        cls=int(box.cls[0]);score=float(box.conf[0])
        severity,ratio=severity_proxy((x2-x1)*(y2-y1),w*h)
        name=MODEL.names[cls]
        color={'Low':'#238b45','Medium':'#e6a100','High':'#cf3030'}[severity]
        draw.rectangle((x1,y1,x2,y2),outline=color,width=max(3,w//250))
        draw.text((x1,max(0,y1-22)),f'{name} | {severity} proxy | {score:.2f}',fill=color)
        rows.append([name,round(score,3),severity,round(ratio,4)])
    note=(f'{len(rows)} defect(s) detected. Severity is an unvalidated image-area proxy, '
          'not a measurement of physical crack width or pothole depth. Human inspection is required.')
    return annotated,rows,note

demo=gr.Interface(fn=inspect,
    inputs=[gr.Image(type='pil',label='Road photograph'),gr.Slider(.05,.8,value=.25,step=.05,label='Detection confidence')],
    outputs=[gr.Image(type='pil',label='Detected defects'),
             gr.Dataframe(headers=['Type','Confidence','Severity proxy','Box area / image'],datatype=['str','number','str','number'],label='Findings'),
             gr.Textbox(label='Interpretation')],
    title='Road Damage Detection — India RDD2022',
    description='Four-class YOLO detector. Low/Medium/High is an illustrative proxy based on image area.')
if __name__=='__main__':demo.launch()
