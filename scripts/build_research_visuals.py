"""Build the CrowdSense video demo. Usage: python scripts/build_research_visuals.py PATH_TO_CROWDSENSE

Requires Pillow, numpy and opencv-python. Uses existing video outputs, not fresh inference.
"""
from pathlib import Path
import sys
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
BG, INK, MUTED = '#152b3c', '#e7f0e5', '#abc6c9'

if len(sys.argv)>1:
    media=Path(sys.argv[1])/'media'
    names=['crowd_vid1.mp4','density.mp4','overlay.mp4']
    caps=[cv2.VideoCapture(str(media/n)) for n in names]
    assert all(c.isOpened() for c in caps)
    assert all(int(c.get(cv2.CAP_PROP_FRAME_COUNT))==341 for c in caps)
    fonts=Path('C:/Windows/Fonts')
    font=lambda size: ImageFont.truetype(str(fonts/'segoeui.ttf'),size)
    heading, label, small=font(25),font(18),font(15)
    frames=[]
    # Every panel uses the identical source frame index. Six seconds at 8 fps.
    for i in range(48):
        frame_index=25+round(i*25/8)
        canvas=Image.new('RGB',(960,330),BG); draw=ImageDraw.Draw(canvas)
        draw.text((24,15),'CrowdSense',font=heading,fill=INK)
        draw.text((192,24),'One scene, three views',font=small,fill=MUTED)
        for k,(cap,name) in enumerate(zip(caps,['Input video','Predicted density','Density overlay'])):
            cap.set(cv2.CAP_PROP_POS_FRAMES,frame_index)
            ok, frame=cap.read(); assert ok
            im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).resize((296,167),Image.Resampling.LANCZOS)
            x=24+k*308
            draw.text((x,66),name,font=label,fill=INK)
            canvas.paste(im,(x,98))
        draw.line((24,282,936,282),fill='#35515e',width=2)
        draw.line((24,282,24+int(912*(i+1)/48),282),fill='#91d2c1',width=3)
        draw.text((24,300),'Existing CrowdSense demo outputs · synchronized frames',font=small,fill=MUTED)
        draw.text((788,300),f'{frame_index/25:04.1f}s / video',font=small,fill=MUTED)
        frames.append(canvas)
    for cap in caps: cap.release()
    frames[16].save(OUT/'crowdsense-demo.png',optimize=True)
    palette=frames[16].quantize(colors=128)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT/'crowdsense-demo.gif',save_all=True,append_images=indexed[1:],duration=125,loop=0,optimize=True)
    print('GIF bytes:',(OUT/'crowdsense-demo.gif').stat().st_size)
print('Visuals written to',OUT)
